import ipyvuetify as v
from matplotlib.style import context
from components.cards import BaseCard
from utils import get_or_create_class
from components.forms import DataSelect, DataSlider, LabeledSelect, SimpleSlider
from components.buttons import StatedBtn
from components.layouts import IndexRow
from components.cards import SmallHeaderCard
from components.dialog import BaseDialog
import logging
from ludwig.api import LudwigModel
import ipywidgets as widgets
from IPython.display import display
import shutil
import os   
from utils import delete_files_in_dir

class TabularModel:
    def __init__(
        self, 
        app_context: object = None,
        context_key: str = None,
        config: dict = None,
        output: object = None,
        logging_level: object = None,
        **kwargs
        ):

        self.config = config
        self.output = output
        self.logging_level = logging_level
        self.data = app_context.current_data
        self.data_name = app_context.current_data_name
        self.model_name = 'latest'
        self.output_directory = 'train_test'
        self.output_model_directory = os.path.join(self.output_directory, f'{self.data_name}_{self.model_name}')

        # temporary for testing
        if os.path.exists(self.output_directory):
            delete_files_in_dir(self.output_directory)
        else:
            os.makedirs(self.output_directory)

    def train(self):
        if os.path.isdir(self.output_model_directory):
            shutil.rmtree(self.output_model_directory)
            self.output.clear_output()

        self.model = LudwigModel(self.config, logging_level = self.logging_level)

        with self.output:
            self.eval_stats, self.train_stats, self.preprocessed_data, self.output_dir = self.model.experiment(
                dataset=self.data, 
                experiment_name=self.data_name, 
                model_name=self.model_name,
                output_directory=self.output_directory,
                skip_save_processed_input = True,
                skip_save_logs = True,
            )

class TabularTrainActivator(v.Row):
    def __init__(
        self,
        app_context:object = None,
        context_key:str = None,
        title:str = "",
        **kwargs,
    ):
        self.app_context = app_context
        self.style = {
            'row':'width: 1570px; align-self: center;',
            'button':'background-color:#1876d2; color:#ffffff;'
            } 

        self.train_activator = v.Btn(
            children = ['학습하기'],
            style_ = self.style['button'],
        )
        
        def _activate_model_train(item, event=None, data=None):
            config = self.app_context.tabular_ai_training__modeling_options.retrieve_config()
            train_result = self.app_context.tabular_ai_training__train_result
            train_result.show()

            self.model = get_or_create_class(
                'tabular_model',
                self.app_context,
                config = config,
                output = train_result.output_logs,
                logging_level = logging.INFO,
            )
            
            self.model.train() 
            train_result.organize_charts()
            train_result.select_chart_view.disabled = False

        self.train_activator.on_event('click', _activate_model_train)

        super().__init__(
            children = [self.train_activator],
            style_ = self.style['row'],
        )

class TabularTrainResult(BaseDialog):
    def __init__(
        self, 
        app_context:object = None,
        context_key:str = "",
        title:str = "",
        **kwargs,
        ):
        self.app_context = app_context
        self.style = {}

        # result ouput for training result
        self.output_logs = widgets.Output(
        )   
        self.output_plots = v.Container(
            children = [""],
        )

        body_items = [self.output_logs]

        # select options
        self.select_text_view = v.Btn(
                    small = True,
                    plain = True,
                    depressed = True,
                    text = True,
                    disabled = True,
                    children = ['텍스트 로그'],
                    style_ = 'color:rgb(0,0,0, 0.87) !important;',
                )

        self.select_chart_view = v.Btn(
                    small = True,
                    plain = True,
                    depressed = True,
                    text = True,
                    disabled = True,
                    children = ['차트 보기'],
                    style_ = 'color:rgb(0,0,0, 0.87) !important;',
                )

        def _on_select_chart_view(item, event=None, data=None):
            pass

        def _on_select_text_view(item, event=None, data=None):
            pass


        self.select_chart_view.on_event('click', _on_select_chart_view)
        self.select_text_view.on_event('click', _on_select_text_view)


        self.selector = v.Row(
            style_ = "margin: 0px; width:100%; max-height:33px; padding:0 12px; background-color:#f1f1f1; border-top:1px solid #e0e0e0;",
            children = [self.select_text_view, self.select_chart_view],
        )

        super().__init__(
            v_slots = [{
                # 'name': 'activator',
                # 'variable': 'x',
                # 'children': train_button,
                }],
            header_title = '학습 결과',
            header_bottom = self.selector,
            body_items = body_items,
            body_size = {'width': '90vw', 'height': ['80vh']},
            body_border_bottom = [True],
            body_background_color = ["rgb(255, 255, 255)"],
            align = 'center',
            more = False,
            close = True,
            class_ = context_key,
            app_context = self.app_context,
            selector = self.selector,
        )    

    def show(self):
        self.value = 1
        self.value = 2

    def close(self):
        self.value = 0

    def organize_charts(self):
        pass

class TabularModelingOptions(BaseCard):
    def __init__(
        self, 
        app_context:object = None,
        context_key:str = "",
        title:str = "",
        **kwargs,
        ):   

        self.style = {
            'column_options_body': "padding:0px;",
            'column_options_body_item': "min-height:62px; padding:0", 
        }

        self.app_context = app_context
        self.data = app_context.current_data

        # re-structure data for column-wise configuration
        num_rows = len(self.data.columns)
        config= self.app_context.modeling_params['ludwig']['config']

        # column options header ----------------------------------------------------------
        column_options_header_texts = [
            {"name":"입/출력", "style":"max-width:68px; text-align:center;"},
            {"name":"칼럼명", "style":"text-align:left; padding-left:40px; max-width:200px;"},
            {"name":"데이터 유형", "style":"min-width:327px; text-align:left;"},
        ]
        column_options_header = v.Row(
            style_ = "margin: 0px; width:100%; max-height:33px; padding:0 12px; background-color:#f1f1f1; border-top:1px solid #e0e0e0;",
            children = [
                v.Col(
                    style_ = 'font-size: 0.875rem; color:rgb(100, 116, 139); padding:0px;' + text['style'],
                    children = [text['name']],
                    ) for text in column_options_header_texts] 
        )

        # column options body -------------------------------------------------------------

         # reset data options body_rows when data is changed
        def _ignore_data_row(index):
            data_types[index].items = []
            data_types[index].v_model = None
            encoder_or_model_types[index].items = []
            encoder_or_model_types[index].v_model = None
            self.column_options_rows[index].children[5].children = []

        def _change_additional_options(index: int):
            in_out_ignore = in_out_ignore_buttons[index].v_slots[0]['children'][0].state
            data_type = data_types[index].v_model
            encoder_or_model_type = encoder_or_model_types[index].v_model
            additional_option_dict = _get_additional_option(in_out_ignore, data_type, encoder_or_model_type)
            self.column_options_rows[index].children[5].children = _make_additional_option_widget_row(index, additional_option_dict)

        def _change_encoder_or_model_type(index: int):
            in_out_ignore = in_out_ignore_buttons[index].v_slots[0]['children'][0].state
            data_type = data_types[index].v_model
            encoder_or_model_type = "encoder" if in_out_ignore == "input" else "model_type"

            encoder_or_model_types[index].items = config[in_out_ignore][encoder_or_model_type][data_type]['values'] 
            encoder_or_model_types[index].v_model = config[in_out_ignore][encoder_or_model_type][data_type]['default'] 
            encoder_or_model_types[index].readonly = True if len(encoder_or_model_types[index].items) == 1 else False

            _change_additional_options(index)

        def _change_data_types(index: int):
            in_out_ingore = in_out_ignore_buttons[index].v_slots[0]['children'][0].state
            pandas_data_type = pandas_data_types[index].v_model

            data_types[index].items = config[in_out_ingore]['dtype'][pandas_data_type]['values']
            data_types[index].v_model = config[in_out_ingore]['dtype'][pandas_data_type]['default']
            data_types[index].readonly = True if len(data_types[index].items) == 1 else False

            _change_encoder_or_model_type(index)

        # (1) in_out_ignore buttons ---------------------------------------------
        def _on_click_in_out_ignore(item, event=None, data=None):
            index = int(item.index)

            if item.state == 'input':
                new = {'state':'output', 'icon':'mdi-arrow-left-circle', 'text':"출력"}
            elif item.state == 'output':
                new = {'state':'ignore', 'icon':'mdi-close-circle', 'text':"제외"}
            else:
                new = {'state':'input', 'icon':'mdi-arrow-right-circle-outline', 'text':"입력"}

            # change state, icon & text
            item.state = new['state']
            item.children[0].children = [new['icon']]
            in_out_ignore_buttons[index].children = [new['text']]
            
            # change subordinate data
            if item.state != 'ignore':
                _change_data_types(index)
            else:
                _ignore_data_row(index)

        def _make_tooltip_button(index):
            btn = StatedBtn(
                index = index,
                state = 'input',
                v_on='tooltip.on',
                icon = True,
                style_ = "margin-left:24px; margin-top:14px; margin-right:22px;",
                children = [v.Icon(children = "mdi-arrow-right-circle-outline")],
            )
            btn.on_event('click', _on_click_in_out_ignore)
            return btn

        in_out_ignore_buttons = [
            v.Tooltip(
                right=True, 
                v_slots=[{
                    'name': 'activator',
                    'variable': 'tooltip',
                    'children': [_make_tooltip_button(str(i))],
                }],
                children = ['입력']
            ) for i in range(num_rows)
        ]

        # (2) column_names ------------------------------------------------------
        column_names = [
            v.Col(
                class_ = '',
                children = [column_name],
                style_ = "font-size:1rem; padding-top:22px; padding-bottom:5px; padding-right:15px; max-width:200px; min-width:200px; \
                    white-space:nowrap; overflow:hidden; text-overflow:ellipsis;",
            ) for column_name in self.data.columns
        ]

        # (3) pandas_data_types -------------------------------------------------
        pandas_data_types = [
            v.TextField(
                class_ = str(i),
                v_model = dtype,
                style_ = "display:none;",
            ) for i, dtype in enumerate(self.data.dtypes.apply(lambda x: x.name).to_list())
            
        ]

        # (4) data_type for modeling -------------------------------------------------
        data_types = [
            DataSelect(
                index = str(i),
                items = config['input']['dtype'][dtype.v_model]['values'],
                v_model = config['input']['dtype'][dtype.v_model]['default'],
                dense = True,
                style_ = "max-width:150px; margin-right:24px;",
                readonly = True if len(config['input']['dtype'][dtype.v_model]['values']) == 1 else False
            ) for i, dtype in enumerate(pandas_data_types)
        ]

        def _on_select_data_type(item, event=None, data=None):
            index = int(item.index)
            _change_encoder_or_model_type(index)

        for item in data_types:
            item.on_event('change', _on_select_data_type)

        # (5) input: encoder / output: model type--------------------------------
        encoder_or_model_types = [
            DataSelect(
                index = str(i),
                items = config['input']['encoder'][dtype.v_model]['values'],
                v_model = config['input']['encoder'][dtype.v_model]['default'],
                dense = True,
                style_ = "max-width:150px; margin-right:24px;",
                readonly = True if len(config['input']['encoder'][dtype.v_model]['values']) == 1 else False
            ) for i, dtype in enumerate(data_types)
        ]

        def _on_select_encoder_or_model_type(item, event=None, data=None):
            index = int(item.index)
            _change_additional_options(index)

        for item in encoder_or_model_types:
           item.on_event('change', _on_select_encoder_or_model_type)

        # (6) additional options--------------------------------
        def _get_additional_option(in_out_ignore, data_type, encoder_or_model_type):
            return config[in_out_ignore]['additional_config'][data_type][encoder_or_model_type]

        def _make_additional_option_widget_row(index, additional_option_dict):
            additional_option_widgets = []
            for additional_option in additional_option_dict.items():
                if additional_option[0] == 'activation':
                    widget = LabeledSelect(
                        class_ = additional_option[0],
                        index = str(index),
                        label = "활성 함수",
                        items = additional_option[1]['values'],
                        v_model = additional_option[1]['default'],
                        dense = True,
                        style_ = "max-width:220px; padding: 0; margin: 3px !important; \
                            border-radius: 8px; background-color: #f1f1f1;",
                        readonly = True if len(additional_option[1]['values']) == 1 else False,
                    )
                    additional_option_widgets.append(widget)

                if additional_option[0] == 'representation':
                    widget = LabeledSelect(
                        class_ = additional_option[0],
                        index = str(index),
                        label = "표현 방식",
                        items = additional_option[1]['values'],
                        v_model = additional_option[1]['default'],
                        dense = True,
                        style_ = "max-width:220px; padding: 0; margin: 3px !important; \
                            border-radius: 8px; background-color: #f1f1f1;",
                        readonly = True if len(additional_option[1]['values']) == 1 else False,
                    )
                    additional_option_widgets.append(widget)
                
                if additional_option[0] == 'num_fc_layers':
                    widget = DataSlider(
                        class_ = additional_option[0],
                        index = str(index),
                        label = "FC 레이어 수",
                        range = additional_option[1],
                        dense = True,
                        style_ = "max-width:220px; padding: 0; margin: 3px !important; \
                            border-radius: 8px; background-color: #f1f1f1;",
                    )
                    additional_option_widgets.append(widget)
                
                if additional_option[0] == 'fc_size':
                    widget = DataSlider(
                        class_ = additional_option[0],
                        index = str(index),
                        label = "FC 크기",
                        range = additional_option[1],
                        dense = True,
                        style_ = "max-width:220px; padding: 0; margin: 3px !important; \
                            border-radius: 8px; background-color: #f1f1f1;",
                    )
                    additional_option_widgets.append(widget)

                if additional_option[0] == 'embedding_size':
                    widget = DataSlider(
                        class_ = additional_option[0],
                        index = str(index),
                        label = "임베딩 크기",
                        range = additional_option[1],
                        dense = True,
                        style_ = "max-width:220px; padding: 0; margin: 3px !important; \
                            border-radius: 8px; background-color: #f1f1f1;",
                    )
                    additional_option_widgets.append(widget)

                if additional_option[0] == 'dropout':
                    widget = DataSlider(
                        class_ = additional_option[0],
                        index = str(index),
                        label = "드롭 아웃",
                        range = additional_option[1],
                        dense = True,
                        style_ = "max-width:220px; padding: 0; margin: 3px !important; \
                            border-radius: 8px; background-color: #f1f1f1;",
                    )
                    additional_option_widgets.append(widget)
            return additional_option_widgets
        
        self.additional_option_rows =  [_get_additional_option(            
            in_out_ignore_button.v_slots[0]['children'][0].state, 
            data_type_option.v_model, 
            encoder_or_model_type.v_model
            ) for in_out_ignore_button, data_type_option, encoder_or_model_type in zip(in_out_ignore_buttons, data_types, encoder_or_model_types)
        ]

        self.additional_option_widget_rows = []
        for i, additional_option_dict in enumerate(self.additional_option_rows):
            self.additional_option_widget_rows.append(_make_additional_option_widget_row(i, additional_option_dict))
   
#-------------------------------------------------------------------------------
        self.column_options_rows = [
            IndexRow(
                index = str(i),
                children = [
                    in_out_ignore_buttons[i], column_names[i], pandas_data_types[i], data_types[i], encoder_or_model_types[i],
                    v.Row(
                        children =  self.additional_option_widget_rows[i],
                        style_ = "margin:0;",
                        ),
                ],
                style_ = "min-height:61px; margin:0;",
            ) for i in range(num_rows)

        ]       

        self.last_clicked_column_options_rows = None
        def _on_click_column_options_rows(item, event=None, data=None):
            index = int(item.index)
            if self.last_clicked_column_options_rows != index:
                self.last_clicked_column_options_rows = index
                self.app_context.tabular_ai_training__column_summary.update_data(self.data[column_names[index].children[0]])

        for row in self.column_options_rows:
            row.on_event('click', _on_click_column_options_rows)      


        self.column_options_body = v.List(
            class_ = context_key,
            style_ = self.style['column_options_body'],
            children = [
                v.ListItem(
                    class_ = "modeling-option-table-row",
                    children = [row],
                    dense = True,
                    style_ = self.style['column_options_body_item'],
                ) for row in self.column_options_rows
            ],    
        )

        self.column_options_body.children[-1].style_ = "border-bottom:0px; padding:0"


        # train parameter
        epochs = SmallHeaderCard(
            title = "Epochs",
            body = SimpleSlider(
                        range = [1, 1024, 1, 100],
                    ),
            size = {"width":"260px"}, 
        ) 

        batch_size = SmallHeaderCard(
            title = "Batch Size",
            body = SimpleSlider(
                        range = [1, 1024, 1, 128],
                    ),
            size = {"width":"260px"}, 
        ) 

        early_stop = SmallHeaderCard(
            title = "Early Stop",
            body = SimpleSlider(
                        range = [1, 1000, 1, 5],
                    ),
            size = {"width":"260px"}, 
        ) 

        optimizer = SmallHeaderCard(
            title = "Optimizer",
            body = v.Select(
                        v_model = "adam",
                        items = ['adam', 'rmsprop', 'sgd'],
                        dense = True,
                        style_ = "padding-left:16px;"
                    ),
            size = {"width":"260px"}, 
        ) 

        learning_rate = SmallHeaderCard(
            title = "Learning Rate",
            body = v.TextField(
                        v_model = 0.001,
                        dense = True,
                        style_ = "padding-left:16px;"
                    ),
            size = {"width":"260px"}, 
        ) 

        self.train_parameter = v.Row(
            children = [epochs, batch_size, early_stop, optimizer, learning_rate],
            style_ = "margin:0; height:100%; \
                justify-content: space-around; align-items: center;",
        )

        super().__init__(
            class_ = context_key,
            header_title = title,
            header_bottom  = column_options_header,
            body_items = [
                self.column_options_body, 
                # v.Spacer(style_ = "height:9px; background-color: rgb(241, 245, 249);"),
                self.train_parameter
                ],
            body_size = {
                "width":"1570px",
                "height":["340px", "100px"],
                    },
            body_border_bottom = [True, True],
            body_background_color = ["rgb(255, 255, 255)", "rgb(248, 250, 252)"],
            align = 'center'
        )

    def retrieve_config(self):
        self.train_config = {
            "input_features": [],
            "combiner": {"type":"concat"},
            "output_features": [],
            "preprocessing": {"numerical":{"normalization":"zscore"}},
            "training": {
                "epochs": None,
                "batch_size": None,
                "early_stop": None,
                "optimizer": {"type": "adam"},
                "learning_rate": None,
            },
        }

        def _get_additional_option_config(row):
            additional_option_config = {}
            for widget in row.children[-1].children:
                if widget.__class__.__name__ == 'LabeledSelect':
                    additional_option_config.update(
                        {widget.class_: widget.children[0].children[1].v_model}
                        )
                elif widget.__class__.__name__ == 'DataSlider':
                    additional_option_config.update(
                        {widget.class_: widget.children[0].children[1].v_model}
                        )
            return additional_option_config

        for row in self.column_options_rows:
            additional_option_config = _get_additional_option_config(row)
            if row.children[0].children[0] == "입력":
                self.train_config["input_features"].append(
                    {
                        "name": row.children[1].children[0],
                        "type": row.children[3].v_model,
                        "encoder": row.children[4].v_model,
                        **additional_option_config
                    }
                )
            elif row.children[0].children[0] == "출력":
                self.train_config["output_features"].append(
                    {
                        "name": row.children[1].children[0],
                        "type": row.children[3].v_model,
                        "decoder": row.children[4].v_model,
                        **additional_option_config
                    }
                )

        self.train_config["training"]["epochs"] = self.train_parameter.children[0].children[1].children[0].children[1].v_model
        self.train_config["training"]["batch_size"] = self.train_parameter.children[1].children[1].children[0].children[1].v_model
        self.train_config["training"]["early_stop"] = self.train_parameter.children[2].children[1].children[0].children[1].v_model
        self.train_config["training"]["optimizer"]["type"] = self.train_parameter.children[3].children[1].children[0].v_model
        self.train_config["training"]["learning_rate"] = self.train_parameter.children[4].children[1].children[0].v_model

        return self.train_config