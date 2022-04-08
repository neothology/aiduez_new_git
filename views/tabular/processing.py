import re
import ipyvuetify as v
from utils import get_or_create_class
from components.cards import BaseCard, SimpleCard
from components.forms import DataSelect, SelectAutoComplete
import re
import pandas as pd
from sklearn.preprocessing import MinMaxScaler, StandardScaler, OrdinalEncoder, KBinsDiscretizer, quantile_transform
import plotly.express as px
import os
import ipywidgets
from konlpy.tag import Komoran, Hannanum

class TabularProcessingOptionArea(v.NavigationDrawer):
    def __init__(
        self,
        app_context,
        context_key,
        children,
    ):
        self.children = children
        self.toggle_value = False

        super().__init__(
            style_ = "height:1539px; min-width:220px; max-width:220px; padding-top:8px; background-color:#eeeeee;",
            children = [
                v.Col(
                    children = self.children,
                    style_ = "padding:0; margin:0; display:flex; flex-direction:column; align-items:center",
                )
            ],
            v_model = self.toggle_value,
            class_ = context_key,
            absolute = True,
            temporary = True,
        )
    
    def toggle(self):
        self.toggle_value = not self.v_model

class TabularProcessingSaveActivator(v.Col):
    def __init__(self, app_context:object=None, context_key:str=None, **kwargs) -> None:
        self.app_context = app_context
        self.style = {
            'row': 'display:flex; flex-direction:row; padding:0; padding-top:12px; width:50%; justify-content:flex-end;',
            'data_save_button': 'width:150px; height:35px; background-color:#636efa; color:white;',
            } 

        self.data_save_button = v.Btn(
            style_ = self.style['data_save_button'],
            children = ['가공 데이터 저장'],
            rounded = True,
        )

        def _save_data(widget, event=None, data=None):
            data_name = self.app_context.tabular_dataset.current_data_name + "_preprocessed"
            self.app_context.current_workbook.create_new_work(data_name, self.app_context.tabular_dataset.current_data)

        self.data_save_button.on_event("click", _save_data)
        
        super().__init__(
            children = [self.data_save_button],
            style_ = self.style["row"]
        )

class TabularSingleProcessing(v.Container):
    def __init__(self, app_context, context_key, **kwargs):
        self.app_context = app_context
        self.context_key = context_key

        self.app_context.progress_linear.active = True

        self.column_name=""     # selected column name
        self.process_type=""    # selected process type

        self.processing_options = self._make_single_process_options()

        self.processing_card = get_or_create_class(
                'tabular_data_single_processing_card',
                app_context=self.app_context,
                context_key= 'tabular_data_single_processing__card'
        )   

        self.app_context.progress_linear.active = False

        super().__init__( 
            class_ = self.context_key,
            style_ = "min-width:100%; min-height:100%; background-color:#ffffff; padding:0;",
            children = [
                self.processing_options,
            ],
        )

    def _make_single_process_options(self):
        processing_options = get_or_create_class(
            'tabular_data_processing_options',    # TabularProcessingOptionArea
            self.app_context,
            context_key = 'tabular_data_processing__options',
            children = [],
        )

        single_process_type = {
            x["title"]: x["name"] for x in self.app_context.processing_params["single_process"]["type"]
        }

        # column selector
        column_selector = SelectAutoComplete(
            label="변수",
            v_model="",
            items = list(self.app_context.tabular_dataset.current_data.columns),
            size={'width':'210px', 'height':'70px'},
            style = "margin:5px;",
        )

        column_selector_card = SimpleCard(
            title="변수 선택",
            body=column_selector,
            size = {'width':'210px'},
            style= 'background-color:#ffffff; border-bottom:1px solid #e0e0e0;'
        )

        # preprocess selector
        preprocess_selector = DataSelect(
            index=0,
            items=list(single_process_type.keys()),
            v_model=self.process_type,
            label="가공",
            style_='width:210px; height:70px; margin:5px;',
        )

        preprocess_selector_card = SimpleCard(
            title="가공 선택",
            body=preprocess_selector,
            size = {'width': '210px'},
            style= 'background-color:#ffffff; border-bottom:1px solid #e0e0e0;'
        )
        

        # 칼럼 삭제 버튼
        delete_button = v.Col(
            children= [
                v.Btn(
                    style_ = "",
                    children = ['변수 삭제'],
                    v_model=self.column_name,
                    rounded = True,
                    depressed = True,
                    color = "red lighten-1",
                ),
            ],
            style_ = "margin:0; padding:0; display:flex; flex-direction:row; justify-content:center; align-items:center; width:210px;",
        )

        # 가공하기 버튼
        preprocess_button = v.Col(
            children= [
                v.Btn(
                    style_ = "",
                    children = ['가공하기'],
                    v_model={'column_name': '', 'process': ''},
                    rounded = True,
                    depressed = True,
                    dark = True,
                ),
            ],
            style_ = "margin:0; padding:0; display:flex; flex-direction:row; justify-content:center; align-items:center; width:210px;",
        )

        # column_selector handler
        def _change_column(widget, event=None, data=None):
            config = self.app_context.processing_params['single_process']['config']
            column = self.app_context.tabular_dataset.current_data[widget.v_model]
            self.column_name = widget.v_model
            preprocess_types = config["dtype"][column.dtype.name].keys()
            preprocess_type_titles = [title for title, name in single_process_type.items() if name in preprocess_types]
            preprocess_selector.items = preprocess_type_titles
            preprocess_selector.v_model = preprocess_type_titles[0]
            # preprocess_selector_card's body's children
            preprocess_selector_card.children[1].children = [preprocess_selector]

        column_selector.on_event("change", _change_column)

        # delete_button handler
        def _click_delete_button(widget, event=None, data=None):
            self.app_context.tabular_dataset.current_data = self.app_context.tabular_dataset.current_data.drop(column_selector.v_model, axis=1)
            self.update()
        delete_button.on_event('click', _click_delete_button)

        # preprocess_button handler
        def _click_preprocess_button(widget, event=None, data=None):
            alert = get_or_create_class('alert', self.app_context)
            if column_selector.v_model == '' or preprocess_selector.v_model == '':
                if column_selector.v_model == '':
                    message = "변수를 선택해주세요!"
                else:
                    message = "가공 방식을 선택해 주세요!"
                alert.children = [message]
                alert.type = "error"
                alert.v_model = True
            else:
                alert.v_model = False
                self.app_context.progress_linear.active = True
                self.column_name = column_selector.v_model
                self.process_type = single_process_type[preprocess_selector.v_model]
                self.processing_card.initialize(column_name=self.column_name, process_type=self.process_type)
                self.children = [
                    self.processing_options,
                    self.processing_card
                ]
                self.app_context.progress_linear.active = False
                self.processing_options.v_model = False
            
        preprocess_button.on_event("click", _click_preprocess_button)

        # processing_options -> v.Col -> children
        processing_options.children[0].children = [                
            column_selector_card,
            v.Spacer(style_ = "min-height:10px"),
            preprocess_selector_card,
            v.Spacer(style_ = "min-height:10px"),
            # run_button,
            v.Row(
                children=[delete_button, preprocess_button],
                style_="margin:0; padding:0;"
            ),
        ]
        return processing_options

    def update(self):
        self.app_context.progress_linear.active = True
        self.processing_options = self._make_single_process_options()
        self.children = [
            self.processing_options,
        ]
        self.app_context.progress_linear.active = False
        self.processing_options.v_model = True


class TabularSingleProcessingCard(v.Card):
    def __init__(self, app_context, context_key="", **kwargs) -> None:
        self.app_context = app_context
        self.context_key = context_key

        self.process = ''
        self.method = ''
        self.column_name = ''
        self.column_dtype = ''
        self.suffix = {
            "missing_num_imputer": "IM", "missing_cat_imputer": "IM", "re_extract": "RE",
            "standard_scaler": "SS", "minmax_scaler": "MS", "ordinal_encoder": "OE",
            "quantile_transformer": "QT", "kbins_discretizer": "KD", "형태소 분석": "MA", "명사 추출": "NE",
        }
        self.chart_file_dir = self.app_context.env_values['tmp_dir']+f"/processing_charts/{app_context.tabular_dataset.current_data_name}"
        if not os.path.exists(self.chart_file_dir):
            os.makedirs(self.chart_file_dir)
            
        # method selector
        self.method_selector = v.Select(
            class_="mx-3",
            v_model=self.method,
            label='Method',
            items=[],
            value=self.method,
            attach=True,
        )

        def _change_method(widget, event=None, data=None):
            self.method = widget.v_model
            self.show()
            
        self.method_selector.on_event('change', _change_method)
        
        # additional configs value
        self.additional_config_values = dict()

        # ui
        self.card_contents = None
        self.additional_config_ui = None
        self.before_contents = None
        self.after_contents = None
        
        save_btn = v.Btn(
            color="success",
            children=["새 칼럼으로 저장"]
        )

        def _on_click_save(widget, event=None, data=None):
            # 박영근 추가: progress linear
            self.app_context.progress_linear.active = True

            before_coulumn = self.get_sample_data(column_name=self.column_name, n=-1)
            processed_column = self.processing_data(before_coulumn)
            new_colunm_name = self.column_name + "_" + self.suffix[self.method]
            self.app_context.tabular_dataset.current_data[new_colunm_name] = processed_column
            tabular_data_single_processing = get_or_create_class('tabular_data_single_processing', app_context=self.app_context)
            tabular_data_single_processing.update()
            alert = get_or_create_class('alert', self.app_context)
            alert.children = [f"{new_colunm_name}이 생성되었습니다!"]
            alert.type = "success"
            alert.v_model = True
            
            # 박영근 추가: save workbook
            self.app_context.current_workbook.save_workbook()
            self.app_context.progress_linear.active = False

        save_btn.on_event('click', _on_click_save)

        # card contents
        self.card_title = v.CardTitle(
            primary_title=True,
            children="",
            style_="background-color:rgb(248, 250, 252); border-bottom:1px solid #e0e0e0; height:60px; \
                    font-size:1rem; font-weight:bold; color: rgb(30, 41, 59);"
        )
        self.card_body = v.CardText(
            children=[v.Row(
                style_ = "max-height:100%; margin:0; padding:0; background-color:#ffffff; \
                        display:flex, flex-direction:column;",
                children = [self.method_selector],
            )]
            # children=[self.method_selector],
            # style_="padding:0px; height:100%; background-color:rgb(255, 255, 255);"
        )
        self.card_footer = v.CardActions(
            children=[save_btn],
            style_="background-color:rgb(248, 250, 252); justify-content:flex-end; padding-right:20px; border-top:1px solid #e0e0e0;"
        )

        super().__init__(
            # class_="pa-3",
            children = [self.card_title, self.card_body, self.card_footer],
            style_= "display:flex; flex-direction:column; \
                box-shadow: none !important; border:1px solid #e0e0e0; \
                background-color: rgb(255, 255, 255);"
        )

    def initialize(self, column_name, process_type):
        self.process_type = process_type
        self.column_name = column_name
        config= self.app_context.processing_params['single_process']['config']
        column = self.app_context.tabular_dataset.current_data[column_name]

        self.column_statistic = dict()

        self.column_dtype = column.dtype.name

        if self.column_dtype in ["float64", "int64"]:
            self.column_statistic = {
                "most_frequent": column.mode()[0],
                "median": column.median(),
                "mean": column.mean(),
                "constant": 0,
            }
        elif self.column_dtype == "object":
            self.column_statistic = {
                "most_frequent": column.mode()[0],
                "constant": "",
            }
        method_value = config['dtype'][self.column_dtype][process_type]['default'] if process_type in config['dtype'][self.column_dtype].keys() else []        
        method_items = config['dtype'][self.column_dtype][process_type]['values'] if process_type in config['dtype'][self.column_dtype].keys() else ''
        self.method_selector.items = method_items
        self.method_selector.value = method_value
        self.method_selector.v_model = method_value
        self.method = method_value

        self.show()

    def show(self):
        self.additional_config_ui = self._make_additional_config_ui(self.method, self.column_name)
        self.before_contents = self._make_before_contents(self.column_name)
        self.after_contents = self._make_processed_contents(self.column_name)

        # Card Title
        self.card_title.children = [
            f"{self.column_name.upper()} - {self.process_type.upper()}",
        ]

        self.card_body.children = [
            # method selector
            v.Row(children=[self.method_selector]),
            # additional config
            v.Row(children=[v.Col(children=[ui]) for ui in self.additional_config_ui.values()]),
            # result area
            v.Row(children=[
                # before contents
                v.Col(class_="py-0", children=[self.before_contents]),
                # arrow icon
                v.Icon(
                    large=True,
                    children=["mdi-arrow-right-bold"]
                ),
                # after contents
                v.Col(class_="py-0", children=[self.after_contents]),                                
            ])
        ]
        self.children = [self.card_title, self.card_body, self.card_footer]

    def _make_additional_config_ui(self, method, column_name) -> dict:
        config= self.app_context.processing_params['single_process']['config']
        additional_configs = config['additional_config'][method]['option'] if method in config['additional_config'].keys() else []
        additonal_config_ui = {}    # 추가 설정 UI
        for option in additional_configs:
            self.additional_config_values[option["name"]] = ""
            if option['type'] == "slider":
                self.additional_config_values[option["name"]] = option['values'][3]
                slider = v.Slider(
                    min = option['values'][0],
                    max = option['values'][1],
                    step = option['values'][2],
                    v_model = option['values'][3],
                    label=option['name'],
                    value=option['name'],
                    dense = True,
                    hide_details = True,
                    style_ = "padding:0; height:25px; \
                        margin: 15px 2px 0 8px;",
                )
                counter = v.TextField(
                    v_model = option['values'][3],
                    value=option['name'],
                    filled = True,
                    dense = True,
                    hide_details = True,
                    style_ = "max-width:90px; padding:3px",
                )
                ipywidgets.jslink((slider, 'v_model'), (counter, 'v_model'))
                def _on_change_slider(widget, event=None, data=None):
                    self.additional_config_values[widget.value] = widget.v_model
                    self.after_contents = self._make_processed_contents(column_name)

                    # after contents area
                    self.card_body.children[2].children[2].children = [self.after_contents]
                            
                slider.on_event("change", _on_change_slider)
                counter.on_event("change", _on_change_slider)
                widget = v.Row(children=[slider, counter])
                additonal_config_ui[option['name']] = widget

            elif option['type'] == 'select':
                self.additional_config_values[option["name"]] = option['default']
                widget = v.Select(
                    label=option['name'],
                    items=option['values'],
                    v_model=self.additional_config_values[option["name"]],
                    attach=True,
                )
                def _change_select(widget, event=None, data=None):
                    self.additional_config_values[widget.label] = widget.v_model
                    if self.process_type == "fill" and "value" in self.additional_config_values.keys():
                        self.additional_config_ui["value"].v_model = self.column_statistic[widget.v_model]
                        self.additional_config_values["value"] = self.column_statistic[widget.v_model]
                        if widget.v_model == "constant":
                            self.additional_config_ui["value"].disabled=False
                        else:
                            self.additional_config_ui["value"].disabled=True

                        self.after_contents = self._make_processed_contents(column_name)
                        # result area
                        self.card_body.children[2].children[2].children = [self.after_contents]
                    else:
                        self.additional_config_values[widget.label] = widget.v_model

                        self.after_contents = self._make_processed_contents(column_name)
                        # result area
                        self.card_body.children[2].children[2].children = [self.after_contents]

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
                    if self.process_type == "fill":
                        self.column_statistic[self.additional_config_values["imputer"]] = widget.v_model
                    elif self.process_type == "extract" and self.method == "re_extract":
                        self.additional_config_values["regex"] = widget.v_model
                        
                    self.after_contents = self._make_processed_contents(column_name)
                    self.card_body.children[2].children[2].children = [self.after_contents]
                
                widget.on_event('change', _change_text)
                additonal_config_ui[option['name']] = widget
        return additonal_config_ui

    def get_sample_data(self, column_name, n=1000):
        '''
        n 의 값이 -1이면 전체를 가지고 옴
        '''
        sample_data = self.app_context.tabular_dataset.current_data[column_name]
        if n != -1:
            if self.process_type == "fill":
                sample_data = sample_data[sample_data.isna()]

            if len(sample_data) > n:
                sample_data = sample_data[:n]                

        return sample_data

    def _make_before_contents(self, column_name):
        before_result = v.CardText(
            class_='text-center',
            children=["Before Contents"],
        )

        if self.process_type in ['scale', 'transform'] and self.method != 'ordinal_encoder':
            sample_data = self.get_sample_data(column_name, n=-1)
        else :
            sample_data = self.get_sample_data(column_name, n=15)

        if self.process_type == "fill" and len(sample_data) == 0:
            children = ["Null 값이 없습니다!"]

        elif self.process_type == "scale" or (self.process_type == "transform" and self.method != "ordinal_encoder"):
            chart = self._make_histogram(sample_data, suffix="before")
            children = [chart]
        else:
            children = [v.Html(class_="my-2", tag="h4", children=[v.Text(children=str(value))]) for value in sample_data.values]

        before_result.children = children
        
        contents = v.Card(
            class_="overlow-auto",
            children=[
                v.CardTitle(
                    class_="headline justify-center",
                    primary_title=True,
                    children=["Before"]
                ),
                before_result
        ])

        return contents

    def processing_data(self, column):

        if self.process_type == "fill":
            imputer_value = self.column_statistic[self.additional_config_values["imputer"]]
            try:
                if self.column_dtype.startswith("float"):
                    imputer_value = float(imputer_value)
                elif self.column_dtype.startswith("int"):
                    imputer_value = int(imputer_value)
                self.additional_config_ui["value"].v_model = imputer_value
                column = column.fillna(imputer_value)
            except:
                column = None

        elif self.process_type == "extract" and self.method == "re_extract":
            regex = self.additional_config_values["regex"]
            self.additional_config_ui["regex"].disabled = False
            try:
                column = column.apply(lambda x:" ".join(re.findall(regex, x)))
            except:
                column = None

        elif self.process_type == "scale":
            if self.method == 'standard_scaler':
                scaler = StandardScaler()
            elif self.method == 'minmax_scaler':
                scaler = MinMaxScaler()
            column = pd.Series(scaler.fit_transform(column.values.reshape(-1, 1)).reshape(-1), name=column.name, index=column.index)

        elif self.process_type == "transform":
            if self.method == "ordinal_encoder":
                encoder = OrdinalEncoder()
                column = pd.Series(encoder.fit_transform(column.values.reshape(-1, 1)).reshape(-1), name=column.name, index=column.index)            
            elif self.method == "quantile_transformer":
                output_distribution = self.additional_config_values["output_distribution"]
                n_quantiles = self.additional_config_values["n_quantiles"]
                column = pd.Series(quantile_transform(column.values.reshape(-1, 1), output_distribution=output_distribution, n_quantiles=n_quantiles).reshape(-1), name=column.name, index=column.index)            
            elif self.method == "kbins_discretizer":
                n_bins = self.additional_config_values["n_bins"]
                strategy = self.additional_config_values["strategy"]
                try:
                    kbins = KBinsDiscretizer(n_bins=n_bins, encode="ordinal", strategy=strategy)
                    column = pd.Series(kbins.fit_transform(column.values.reshape(-1, 1)).reshape(-1), name=column.name, index=column.index)            
                except:
                    column = None
        elif self.process_type == "nlp":
            nlp_package = {
                "komoran": Komoran(),
                "hannanum": Hannanum(),
            }
            nlp_package = nlp_package[self.additional_config_values["package"]]
            column = column.apply(lambda x: self.nlp_processing(string=x, nlp_package=nlp_package, nlp_method=self.method))
        return column

    def _make_processed_contents(self, column_name):
        processed_result = v.CardText(
            class_='text-center',
            children=["After Contents"],
        )

        if self.process_type in ['scale', 'transform']:
            sample_data = self.get_sample_data(column_name, n=-1)
        else:
            sample_data = self.get_sample_data(column_name, n=15)

        sample_processed_data = self.processing_data(sample_data)
        children = []
        if self.process_type == "fill" and sample_processed_data is None:
            children = ["데이터 타입에 맞게 입력해주세요!"]
        elif self.process_type == "fill" and len(sample_processed_data) == 0:
            children = ["Null 값이 없습니다!"]
        elif self.process_type == "extract" and sample_processed_data is None:
            children = ["정규표현식이 올바르지 않습니다!"]
        elif self.process_type == "transform" and self.method == "kbins_discretizer" and sample_processed_data is None:
            children = ["먼저, Null 값을 제거해주세요!"]
        elif self.process_type == "scale":
            chart = self._make_histogram(sample_processed_data, suffix="processed")
            children = [chart]
        elif self.process_type == "transform":
            if self.method == "ordinal_encoder":
                sample_processed_data = sample_processed_data[:15] if len(sample_processed_data) > 15 else sample_processed_data
                children = [v.Html(class_="my-2", tag="h4", children=[v.Text(children=str(value))]) for value in sample_processed_data.values]
            else:
                chart = self._make_histogram(sample_processed_data, suffix="processed")
                children = [chart]
        else:
            children = [v.Html(class_="my-2", tag="h4", children=[v.Text(children=str(value))]) for value in sample_processed_data.values]

        processed_result.children = children
        
        contents = v.Card(
            class_="overlow-auto",            
            children=[
                v.CardTitle(
                    class_="headline justify-center",
                    primary_title=True,
                    children=["After"]
                ),
                processed_result
            ]
        )
        return contents

    def _make_histogram(self, sample_data, suffix):
        char_file_name = self.chart_file_dir + f"/{self.column_name}_{self.method}_{suffix}.html"
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
        return chart 

    def nlp_processing(self, string, nlp_package, nlp_method):
        """
        :param string: string for nlp
        :param nlp_package: "tag.Komoran()", "tag.Kkma()", "tag.Hannanum()", "tag.Okt()"
        :param nlp_method: "nouns", "morphs"
        """
        try:
            if nlp_method == "형태소 분석":
                result = ' '.join(nlp_package.morphs(string))
            elif nlp_method == "명사 추출":
                result = ' '.join(nlp_package.nouns(string))
        except:
            result = string
        return result

class TabularMultipleProcessing(v.Container):
    def __init__(self, app_context, context_key, **kwargs):
        self.app_context = app_context
        self.context_key = context_key

        self.processing_menu = BaseCard(
            app_context=self.app_context,
            context_key=self.context_key,
            title="복합칼럼변환"
        )
        super().__init__(
            # style_ = "min-width:100%; min-height:100%; display:flex; flex-direction:column;",
            children = [
                v.Col(
                    children=[
                        self.processing_menu
                    ]
                )
            ],
        )
