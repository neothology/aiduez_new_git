import re
import ipyvuetify as v
from utils import get_or_create_class
from components.tab import BaseTab
from components.cards import BaseCard, SmallHeaderCard
from components.forms import DataSelect, LabeledSelect, SimpleSlider, DataSlider
from components.buttons import StatedBtn
from components.layouts import IndexRow
import re
import pandas as pd
from sklearn.preprocessing import MinMaxScaler, StandardScaler
import plotly.express as px
import os

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

        self.processing_dialog = get_or_create_class(
            'tabular_data_single_processing_dialog',
            app_context=self.app_context,
            context_key= 'tabular_data_single_processing_dialog'
        )
        # column summary
        self.column_summary = self._get_column_sumary()

        super().__init__(
            class_ = self.context_key,
            style_ = "min-width:100%; min-height:100%; display:flex; flex-direction:column;",
            children = [
                v.Col(
                    class_="d-lg",
                    children=[
                        self.processing_menu,
                        self.processing_dialog,
                        v.Spacer(style_="height:20px"),
                        self.column_summary,
                    ]
                )
            ],
        )

    def _get_column_sumary(self):
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
                    delete_column_buttons[i], column_names[i], pandas_data_types[i],
                    processing_method_buttons[i]['fill'],
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
        def _activate_process_dialog(widget=None, event=None, data=None):
            column_name = widget.v_model["column_name"]
            process = widget.v_model["process"]
            # dialog = self.app_context.tabular_data_single_processing_dialog
            dialog = get_or_create_class(
                'tabular_data_single_processing_dialog',
                app_context=self.app_context,
            )
            # TabularSingleProcessingDialog(app_context=self.app_context, context_key=self.context_key, column=column, process=process)
            def _close_dialog(widget, event=None, data=None):
                widget.value = 0

            dialog.on_event('click:outside', _close_dialog)
            dialog.initialize(column_name=column_name, process=process)

        for col_name in self.data.columns:
            process_type_dialog = {
                'fill': None,
                'transform': None,
                'extract': None,
                'scale': None,
                'nlp': None,
            }

            dtype = self.data[col_name].dtype.name
            for process in process_type_dialog.keys():
                disabled = True
                if process in config['dtype'][dtype].keys():
                    disabled=False
                process_type_dialog[process] = v.Btn(
                    v_model={'column_name': col_name, 'process': process},
                    class_='mx-2',
                    color='blue lighten-5',
                    disabled=disabled,
                    children=[process],
                )

                process_type_dialog[process].on_event('click', _activate_process_dialog)       

            dialog_buttons.append(process_type_dialog)

        return dialog_buttons

class TabularSingleProcessingDialog(v.Dialog):
    def __init__(self, app_context, context_key) -> None:
        self.app_context = app_context

        self.dialog_contents = ''
        self.process = ''
        self.method = ''
        self.column_name = ''
        self.char_file_dir = self.app_context.env_values['tmp_dir']+f"/processing_charts/{self.app_context.current_data_name}"
        if not os.path.exists(self.char_file_dir):
            os.makedirs(self.char_file_dir)
        # close button
        self.close_btn = v.Btn(
            icon=True,
            children=[v.Icon(children=['mdi-close'])],
        )
        def _close_dialog(widget, event=None, data=None):
            self.value = 0
            
        self.close_btn.on_event('click', _close_dialog)

        # method selector
        self.method_selector = v.Select(
            v_model=self.method,
            label='Method',
            items=[],
            value=self.method,
        )

        def _change_method(widget, event=None, data=None):
            # print(f"[_change_method] self.method={self.method}")
            self.method = widget.v_model
            self.show()
            
        self.method_selector.on_event('change', _change_method)
        
        # additional configs value
        self.additional_config_values = dict()

        # dialog contents
        self.dialog_contents = v.Card(children=[
            v.CardTitle(
                class_='headline grey lighten-2',
                primary_title=True,
                children=[
                    "Card Title",
                    v.Spacer(),
                    self.close_btn,
                ],
            ),
            v.CardText(children=[self.method_selector]),
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

        super().__init__(
            class_="d-flex",
            style_="height:100%; width:100%;",
            children=[self.dialog_contents],
            min_width=700,
            max_width=1200,
            value=0,
        )

    def initialize(self, column_name, process):
        # print(f"[initialize] column_name={column_name}, process={process}")
        self.process = process
        self.column_name = column_name
        config= self.app_context.processing_params['single_process']['config']
        column = self.app_context.current_data[column_name]

        self.column_statistic = dict()

        dtype = column.dtype.name

        if dtype in ["float64", "int64"]:
            self.column_statistic = {
                "most_frequent": column.mode()[0],
                "median": column.median(),
                "mean": column.mean(),
                "constant": 0,
            }
        elif dtype == "object":
            self.column_statistic = {
                "most_frequent": column.mode()[0],
                "constant": "",
            }

        method_value = config['dtype'][dtype][process]['default'] if process in config['dtype'][dtype].keys() else []        
        method_items = config['dtype'][dtype][process]['values'] if process in config['dtype'][dtype].keys() else ''

        self.method_selector.items = method_items
        self.method_selector.value = method_value
        self.method_selector.v_model = method_value
        self.method = method_value

        self.show()

    def close(self):
        self.value=0

    def show(self):
        # print(f"[show] self.column_name={self.column_name}, self.process={self.process}")
        self.additional_config_ui = self._make_additonal_config_ui(self.method, self.column_name)
    
        self.before_contents = self._make_before_contents(self.column_name)
        self.after_contents = self._make_processed_contents(self.column_name)

        # Card Title
        self.dialog_contents.children[0].children = [
            f"{self.column_name.upper()} - {self.process.upper()}",
            v.Spacer(),
            self.close_btn,
        ]

        # Card Text
        self.dialog_contents.children[1].children = [
            # method selector
            v.Row(children=[self.method_selector]),
            # additional config
            v.Row(children=[v.Col(children=[ui]) for ui in self.additional_config_ui.values()]),
            # result area
            v.Row(children=[
                v.Col(children=[self.before_contents]),
                v.Icon(
                    large=True,
                    children=["mdi-arrow-right-bold"]
                ),
                v.Col(children=[self.after_contents]),                                
            ])
        ]

        self.value = 1

    def _make_additonal_config_ui(self, method, column_name) -> dict:
        config= self.app_context.processing_params['single_process']['config']
        additional_configs = config['additional_config'][method]['option'] if method in config['additional_config'].keys() else []
        additonal_config_ui = {}

        for option in additional_configs:
            self.additional_config_values[option["name"]] = ""
            if option['type'] == "slider":
                widget = DataSlider(
                    index=0,
                    v_model=self.additional_config_values[option["name"]],
                    label=option['name'],
                    range=option['values'],
                    dense=True,
                )
                additonal_config_ui[option['name']] = widget

            elif option['type'] == 'select':
                self.additional_config_values[option["name"]] = option['default']
                widget = v.Select(
                    label=option['name'],
                    items=option['values'],
                    v_model=self.additional_config_values[option["name"]]
                )
                def _change_select(widget, event=None, data=None):
                    self.additional_config_values[widget.label] = widget.v_model
                    if self.process == "fill" and "value" in self.additional_config_values.keys():
                        self.additional_config_ui["value"].v_model = self.column_statistic[widget.v_model]
                        self.additional_config_values["value"] = self.column_statistic[widget.v_model]
                        if widget.v_model == "constant":
                            self.additional_config_ui["value"].disabled=False
                        else:
                            self.additional_config_ui["value"].disabled=True

                        self.after_contents = self._make_processed_contents(column_name)
                        # result area
                        self.dialog_contents.children[1].children[2].children[2].children = [self.after_contents]
                        
                widget.on_event('change', _change_select)
                additonal_config_ui[option['name']] = widget

            elif option['type'] == 'text':
                self.additional_config_values[option["name"]] = option['value']
                widget = v.TextField(
                    label="value",
                    placeholder="기입 후 Enter키를 눌러주세요",
                    hint="기입 후 Enter키를 눌러주세요",
                    disabled=True,
                    v_model=self.additional_config_values[option["name"]]
                )
                def _change_text(widget, event=None, data=None):
                    self.additional_config_values[widget.label] = widget.v_model
                    if self.process == "fill":
                        self.column_statistic[self.additional_config_values["imputer"]] = widget.v_model
                    elif self.process == "extract" and self.method == "re_extract":
                        self.additional_config_values["regex"] = widget.v_model
                        
                    self.after_contents = self._make_processed_contents(column_name)
                    self.dialog_contents.children[1].children[2].children[2].children = [self.after_contents]
                
                widget.on_event('change', _change_text)
                additonal_config_ui[option['name']] = widget
        return additonal_config_ui

    def get_sample_data(self, column_name, target="sample"):
        sample_data = self.app_context.current_data[column_name]
        if target == "sample":
            if self.process == "fill":
                sample_data = sample_data[sample_data.isna()]

            if len(sample_data) > 20:
                sample_data = sample_data[:20]

        return sample_data

    def _make_before_contents(self, column_name):
        before_result = v.CardText(
            class_='text-center',
            children=["Before Contents"],
            overflow=True,
            style_=f"width:100%; height:100%; padding:0; display:flex; flex-direction:column; "
        )

        if self.process == 'scale':
            sample_data = self.get_sample_data(column_name, target="all")
        else:
            sample_data = self.get_sample_data(column_name, target="sample")

        if self.process == "fill" and len(sample_data) == 0:
            children = ["Null 값이 없습니다!"]

        elif self.process == "scale":
            char_file_name = self.char_file_dir + f"/{self.column_name}_{self.method}_before.html"
            if not os.path.exists(char_file_name):
                fig = px.histogram(sample_data, width=500, height=300)
                fig.update_layout(showlegend=False)
                fig.write_html(char_file_name)
            chart = v.Html(
                class_="mx-auto",
                tag = 'iframe',
                attributes = {
                    'src': os.path.relpath(char_file_name, self.app_context.env_values['workspace_dir']),
                    'style': "border:none; width:100%; height:350px;",

                },
            )
            children = [chart]
            # children = [v.Col(children=[chart], style_="height:100%; width:100%")]
        else:
            children = [v.Html(class_="my-2", tag="h4", children=[v.Text(children=str(value))]) for value in sample_data.values]

        before_result.children = children
        
        contents = v.Card(
            # class_="d-flex",
            style_="width=100%; height=100%",
            children=[
                v.CardTitle(
                    class_="headline justify-center",
                    primary_title=True,
                    children=["Before"]
                ),
                before_result
        ])

        return contents

    def processing_data(self, column_name):
        '''
        target: ["all", "sample"]
        '''
        if self.process == "scale":
            sample_data = self.get_sample_data(column_name, target="all")
        else:
            sample_data = self.get_sample_data(column_name, target="sample")

        if self.process == "fill":
            imputer_value = self.column_statistic[self.additional_config_values["imputer"]]
            self.additional_config_ui["value"].v_model = imputer_value
            sample_data = sample_data.fillna(imputer_value)

        elif self.process == "extract" and self.method == "re_extract":
            regex = self.additional_config_values["regex"]
            self.additional_config_ui["regex"].v_model = regex
            self.additional_config_ui["regex"].disabled = False
            try:
                sample_data = sample_data.apply(lambda x:" ".join(re.findall(regex, x)))
            except:
                sample_data = None
        elif self.process == "scale":
            if self.method == 'standard_scaler':
                scaler = StandardScaler()
            elif self.method == 'minmax_scaler':
                scaler = MinMaxScaler()
            sample_data = pd.Series(scaler.fit_transform(sample_data.values.reshape(-1, 1)).reshape(-1), name=sample_data.name, index=sample_data.index)

        return sample_data

    def _make_processed_contents(self, column_name):
        processed_result = v.CardText(
            class_='text-center',
            children=["After Contents"],
            style_=f"width:100%; height:100%; padding:0; display:flex; flex-direction:column; "
        )

        sample_processed_data = self.processing_data(column_name)

        if self.process == "fill" and len(sample_processed_data) == 0:
            children = ["Null 값이 없습니다!"]

        elif self.process == "extract" and sample_processed_data is None:
            children = ["정규표현식이 올바르지 않습니다!"]

        elif self.process == "scale":
            char_file_name = self.char_file_dir + f"/{self.column_name}_{self.method}_processed.html"
            if not os.path.exists(char_file_name):
                fig = px.histogram(sample_processed_data, width=500, height=300)
                fig.update_layout(showlegend=False)
                fig.write_html(char_file_name)
            chart = v.Html(
                class_="mx-auto",
                tag = 'iframe',
                attributes = {
                    'src': os.path.relpath(char_file_name, self.app_context.env_values['workspace_dir']),
                    'style': "border:none; width:100%; height:350px;",

                },
            )
            children = [chart]
        else:
            children = [v.Html(class_="my-2", tag="h4", children=[v.Text(children=str(value))]) for value in sample_processed_data.values]

        processed_result.children = children
        
        contents = v.Card(children=[
            v.CardTitle(
                class_="headline justify-center",
                primary_title=True,
                children=["After"]
            ),
            processed_result
        ])
        return contents


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