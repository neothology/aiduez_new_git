from faulthandler import disable
from re import M
from turtle import width
from click import style
import ipyvuetify as v
from utils import get_or_create_class
from components.tab import BaseTab
from components.cards import BaseCard, SimpleHeaderCard
from components.forms import DataSelect, SimpleSlider
from components.buttons import StatedBtn
from components.layouts import IndexRow

class TabularProcessingTab(BaseTab):
    def __init__(self, app_context, context_key, **kwags) -> None:
        self.app_context = app_context
        # side tab
        tab_menus = []
        tab_items = []
        for stage in self.app_context.workflows_list['tabular']['stages']:
            if stage['title'] == "데이터 가공":
                for menu in stage['menu_list']:
                    tab_menus.append(menu["title"])
                    tab_items.append(menu["target"])
                break
        super().__init__(
            app_context=app_context,
            context_key=context_key,
            tab_menus=tab_menus,
            tab_items=tab_items,
            vertical=True,
            centered=False,
        )

class TabularSingleProcessing(v.Container):
    def __init__(self, app_context, context_key, **kwargs):
        self.app_context = app_context
        self.context_key = context_key

        # code_will_be_deleted: load test data for tabular modeling
        self.app_context.current_data_name = ('titanic_train')
        import pandas as pd
        self.app_context.current_data = pd.read_csv('data/titanic_train.csv')

        self.data = app_context.current_data

        self.processing_menu = TabularSingleProcessingMenu(
            app_context=self.app_context,
            context_key=self.context_key,
            title="단일칼럼변환"
        )

        # column summary
        self.column_summary = self._get_column_sumary()

        super().__init__(
            class_ = self.context_key,
            style_ = "min-width:100%; min-height:100%; display:flex; flex-direction:column;",
            children = [
                v.Col(
                    class_="d-lg",
                    children=[self.processing_menu,
                    v.Spacer(style_="height:20px"),
                    self.column_summary,
                    ]
                )
            ],
        )

    def _get_column_sumary(self):
        print(self.data.columns)
        initial_column_name = self.data.columns[0]
        column_summary = get_or_create_class(
            'column_summary',
            self.app_context,
            context_key = 'tabular_data_processing_column_summary',
            title = '데이터 요약',
            col = self.data[initial_column_name],
        )
        return column_summary

    def update_display(self):
        self.data = self.app_context.current_data
        self.processing_menu.update()
        # column summary
        self.column_summary = self._get_column_sumary()

        self.children = [v.Col(
                    class_="d-lg",
                    children=[self.processing_menu,
                    v.Spacer(style_="height:20px"),
                    self.column_summary,
        ])]

class TabularSingleProcessingMenu(BaseCard):
    def __init__(self, app_context: object = None, context_key: str = "", title:str="", **kwargs):
        self.app_context = app_context
        self.data = app_context.current_data
        self.context_key = context_key

        self.style = {
            'processing_options_body': "padding:0px;",
            'processing_options_body_item': "min-height:62px; padding:0", # border-bottom:1px solid #e0e0e0; 
        }

        title = "단일칼럼변환"

        self.processing_ui = self._make_single_processing_ui()
        
        super().__init__(
            class_=context_key,
            header_title=title,
            body_items=[self.processing_ui],
            body_size={
                "width":"lg",
                "height":["340px"],
            },
            body_border_bottom = [True],
            body_background_color = ["rgb(255, 255, 255)"],
            align='center',
            style = self.style
        )

    def update(self):
        # print(self.app_context)
        self.body_items= [self._make_single_processing_ui()]

    def _make_single_processing_ui(self) -> list:
        num_rows = len(self.data.columns)

        # (1) delete column icon ------------------------------------------------------
        delete_column_buttons = self._make_delete_column_buttons()

        # (2) column_names ------------------------------------------------------
        column_names = [
            v.Col(
                class_ = '',
                children = [column_name],
                style_ = "font-size:1rem; max-width:200px; min-width:200px; white-space:nowrap; overflow:hidden; text-overflow:ellipsis;",
            ) for column_name in self.data.columns
        ]


        # (3) pandas_data_types -------------------------------------------------
        pandas_data_types = [
            v.Col(
                class_ = '',
                v_model = dtype,
                style_ = "text-align: center; font-size:1rem; max-width:100px; min-width:100px; white-space:nowrap; overflow:hidden; text-overflow:ellipsis;",
                children= [dtype]
            ) for dtype in self.data.dtypes.apply(lambda x: x.name).to_list()
        ]

        # (4) process method button -------------------------------------------------
        processing_method_buttons = self._make_processing_dialog_buttons()

        self.processing_options_rows = [
            IndexRow(
                class_="align-center",
                index = str(i),
                children = [
                    delete_column_buttons[i], column_names[i], pandas_data_types[i], processing_method_buttons[i]['fill'],
                    processing_method_buttons[i]['transform'], processing_method_buttons[i]['extract'],
                    processing_method_buttons[i]['scale'], processing_method_buttons[i]['nlp'],
                ],
                style_ = "min-height:61px; margin:0;",
            ) for i in range(num_rows)
        ]

        self.last_clicked_processing_options_rows = None
        def _on_click_processing_options_rows(item, event=None, data=None):
            index = int(item.index)
            if self.last_clicked_processing_options_rows != index:
                self.last_clicked_processing_options_rows = index
                self.app_context.tabular_data_processing_column_summary.update_data(self.data[self.data.columns[index]])

        for row in self.processing_options_rows:
            row.on_event('click', _on_click_processing_options_rows)

        self.processing_options_body = v.List(
            class_ = self.context_key + " align-center",
            style_ = self.style['processing_options_body'],
            children = [
                v.ListItem(
                    children = [row],
                    dense = True,
                    style_ = self.style['processing_options_body_item'],
                ) for row in self.processing_options_rows
            ],    
        )
        return self.processing_options_body

    def _make_delete_column_buttons(self) -> list:
        delete_column_buttons = []

        def _on_click_delete_column_button(btn, event=None, data=None):
            index= int(btn.index)
            self.data = self.data.drop(self.data.columns[index], axis=1)
            self.app_context.current_data = self.data
            tabular_data_single_processing = get_or_create_class('tabular_data_single_processing', app_context=self.app_context)
            tabular_data_single_processing.update_display()
            
        for i in range(len(self.data.columns)):
            delete_column_button = StatedBtn(
                                        index=i,
                                        state="delete",
                                        icon=True,
                                        color="red lighten-1",
                                        children=[v.Icon(children = ['mdi-delete'])]
            )
            delete_column_button.on_event('click', _on_click_delete_column_button)
            delete_column_buttons.append(delete_column_button)
        return delete_column_buttons

    def _make_processing_dialog_buttons(self) -> list:
        config= self.app_context.processing_params['single_process']['config']

        dialog_buttons = []
        for col in self.data.columns:
            process_type_dialog = {
                'fill': None,
                'transform': None,
                'extract': None,
                'scale': None,
                'nlp': None,
            }

            dtype = self.data[col].dtype.name
            for process in process_type_dialog.keys():
                disabled = True
                method_items = []
                method_value = ''
                if process in config['dtype'][dtype].keys():
                    disabled = False
                    method_items = config['dtype'][dtype][process]['values']
                    method_value = config['dtype'][dtype][process]['default']
                    additional_config_ui = self._make_additonal_config_ui(method_value)
                process_type_dialog[process] = v.Dialog(
                    width="700",
                    v_slots=[{
                        'name': 'activator',
                        'variable': col+'_'+process,
                        'children': v.Btn(
                            class_ ="mx-2",
                            color="blue-grey lighten-5  ",
                            v_on=f"{col+'_'+process}.on",
                            disabled=disabled,
                            children=[process]
                        )
                    }],
                    children=[
                        v.Card(children=[
                            v.CardTitle(
                                class_='headline grey lighten-2',
                                primary_title=True,
                                children=[
                                    f"{col.upper()} {process.upper()}",
                                    v.Spacer(),
                                    v.Btn(
                                        icon=True,
                                        on=f"{col}+'_'+{process}.value = false",
                                        children=[v.Icon(children=['mdi-close'])]
                                    )
                                ],
                            ),
                            v.CardText(children=[
                                # method selector
                                v.Row(
                                    children=[
                                        v.Select(
                                            label='Method',
                                            items=method_items,
                                            value=method_value,
                                        )
                                    ]
                                ),
                                # additional config
                                v.Row(children=[v.Col(children=[ui]) for ui in additional_config_ui]),

                                # result area
                                v.Row(children=[
                                    v.Col(children=[
                                        v.Card(children=[
                                            v.CardTitle(
                                                class_="headline",
                                                primary_title=True,
                                                children=["Before"]
                                            ),
                                            v.CardText(children=["Before Contents"])
                                        ])
                                    ]),
                                    v.Icon(
                                        large=True,
                                        children=["mdi-arrow-right-bold"]
                                    ),
                                    v.Col(children=[
                                        v.Card(children=[
                                            v.CardTitle(
                                                class_="headline",
                                                primary_title=True,
                                                children=["After"]
                                            ),
                                            v.CardText(children=["After Contents"])
                                        ])
                                    ]),                                
                                ])
                            ]),
                            v.CardActions(children=[
                                v.Spacer(),
                                v.Btn(
                                    color="blue lighten-3",
                                    children=["저장"],
                                ),
                                v.Btn(
                                    color="green lighten-3",
                                    children=["새 칼럼 생성"]
                                )
                            ])
                        ])
                    ]
                )

            dialog_buttons.append(process_type_dialog)

        return dialog_buttons

    def _make_additonal_config_ui(self, method) -> list:
        config= self.app_context.processing_params['single_process']['config']
        additional_configs = config['additional_config'][method]['option'] if method in config['additional_config'].keys() else []
        additonal_config_ui = []
        for option in additional_configs:
            if option['type'] == "slider":
                additonal_config_ui.append(
                    SimpleHeaderCard(
                        title = option['name'],
                        body=SimpleSlider(
                            range=option['values'],
                        ),
                    )
                )
            elif option['type'] == 'select':
                additonal_config_ui.append(
                    SimpleHeaderCard(
                        title = option['name'],
                        body=v.Select(
                            items=option['values'],
                            value=option['default']
                        ),
                    )
                )   
        return additonal_config_ui
    
class TabularMultipleProcessing(BaseCard):
    def __init__(self, app_context: object = None, context_key: str = "", title:str="", **kwargs):
        self.app_context = app_context
        self.context_key = context_key
        title = "복합칼럼변환"
        super().__init__(
            class_=context_key,
            header_title=title,
            body_items=[],
            body_size={
                "width":"1570px",
                "height":["340px", "100px"],
            },
            body_border_bottom = [True, True],
            body_background_color = ["rgb(255, 255, 255)", "rgb(248, 250, 252)"],
            align='center'
        )