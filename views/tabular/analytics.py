from email.policy import default

from pyparsing import Word
from numpy import absolute
import pandas as pd
import ipyvuetify as v
import ipywidgets as w
from utils import get_or_create_class

class TabualrAnalyticsOptionArea(v.NavigationDrawer):
    def __init__(
        self,
        app_context,
        context_key,
        children,
    ):
        self.children = children

        super().__init__(
            style_ = "height:1539px; min-width:220px; max-width:220px; padding-top:8px; background-color:#eeeeee;",
            children = [
                v.Col(
                    children = self.children,
                    style_ = "padding:0; margin:0; display:flex; flex-direction:column; align-items:center",
                )
            ],
            v_model = False,
            class_ = context_key,
            absolute = True,
            temporary = True,
        )
    
    def toggle(self):
        self.v_model = not self.v_model


class TabularaAnalyticsBasicinfo(v.Container):
    def __init__(self, app_context, context_key, **kwargs):
        self.app_context = app_context
        self.context_key = context_key

        self.data = self.app_context.tabular_dataset.current_data

        self.result_togle = "display:none;"

        # column selection
        df_col_names = pd.DataFrame(self.data.columns, columns=['col_names'])
        self.column_selector = get_or_create_class(
            'select_table_card',
            self.app_context,
            context_key = f'{self.context_key}__column_selector', # tabular_analytics_basicinfo__column_selector
            title = '변수 선택',
            data = df_col_names,
            size = {'width':'210px', 'height':'200px'},
            style = 'background-color:#ffffff; border-bottom:1px solid #e0e0e0;',
        )
        # column selection - select all
        select_all_values = [{'index':i} for i in range(len(self.data.columns))]
        self.column_selector.children[1].children[0].selected = select_all_values

        # data range selector
        default = 1000 if len(self.data) / 2  > 1000 else len(self.data) / 2
        self.data_range_selector = get_or_create_class(
            'simple_slider_card',
            self.app_context,
            context_key = f'{self.context_key}__data_range_selector', 
            title = '행 범위',
            range = [1, len(self.data), 1, default],
            size = {'width':'210px', 'height':'90px'},
            style = 'background-color:#ffffff; border-bottom:1px solid #e0e0e0;',
        )

        # 조회하기 버튼
        self.run_button = v.Col(
            children= [
                v.Btn(
                    style_ = "",
                    children = ['조회하기'],
                    rounded = True,
                    depressed = True,
                    dark = True,
                ),
            ],
            style_ = "margin:0; padding:0; display:flex; flex-direction:row; justify-content:flex-end; align-items:center; width:210px;",
        )

        self.setting_part = get_or_create_class(
            'tabular_data_analytics_options',
            self.app_context,
            context_key = 'tabular_data_analytics__options',
            children = [
                self.column_selector,
                v.Spacer(style_ = "min-height:10px"),
                self.data_range_selector,
                v.Spacer(style_ = "min-height:10px"),
                self.run_button,
            ],
        )

        self.output_part = v.Row(
            class_ = 'tabular_analytics_basicinfo__output_part',
            style_ = "max-height:100%; margin:0; padding:0; background-color:#ffffff; \
                      display:flex, flex-direction:column;",
            children = [self.setting_part],
        )

        super().__init__(
            class_ = self.context_key,
            style_ = "min-width:100%; min-height:100%; padding:0; display:flex; flex-direction:row; background-color:#ffffff00;",
            children = [
                self.output_part
                ],
        )

        def _show_base_info(item, event, data):
            self.app_context.progress_linear.active = True

            # selected col_names
            selected_cols = self.app_context.tabular_analytics_basicinfo__column_selector.children[1].children[0].selected
            if len(selected_cols) == 0:
                raise Exception('변수를 1개 이상 선택해주세요.')
            selected_cols_to_idx = [col['index'] for col in selected_cols]
            
            # data range
            selected_num_rows = int(self.app_context.tabular_analytics_basicinfo__data_range_selector.children[1].children[0].children[0].v_model)

            # data
            self.df = self.app_context.tabular_dataset.current_data.iloc[:selected_num_rows, selected_cols_to_idx]
           
            # make output & show
            self.data_info = get_or_create_class(
                'data_info',
                self.app_context,
                context_key = f'{self.context_key}__data_info', # tabular_analytics_basicinfo__data_info
                data_name = self.app_context.tabular_dataset.current_data_name,
                data = self.df,
                update = True,
            )

            self.columns_info = [
                get_or_create_class(
                    'column_summary_simple',
                    self.app_context,
                    context_key = f'{self.context_key}__column_summary_simple', # tabular_analytics_basicinfo__column_summary_simple
                    title = f'변수명: {col_name}',
                    col = self.df[col_name],
                    update = True,
                ) for col_name in self.df.columns
            ]

            self.setting_part.v_model = False
            self.output_part.children = [
                self.setting_part, 
                v.Col(
                    children = [self.data_info] + self.columns_info,
                    style_ = "margin:0; padding:0; display:flex; flex-direction:column; max-height:1539px; overflow-y:auto; \
                              padding-top:15px; padding-left:15px",
                ),
            ]
            self.app_context.progress_linear.active = False

        self.run_button.on_event('click', _show_base_info)

class TabularAnalyticsScatter(v.Container):
    def __init__(self, app_context, context_key, **kwargs):
        self.app_context = app_context
        self.context_key = context_key
        super().__init__(
            style_ = "min-width:100%; min-height:100%; display:flex; flex-direction:column;",
            children = [self.context_key]
        )

class TabularAnalyticsHeatmap(v.Container):
    def __init__(self, app_context, context_key, **kwargs):
        self.app_context = app_context
        self.context_key = context_key
        super().__init__(
            style_ = "min-width:100%; min-height:100%; display:flex; flex-direction:column;",
            children = [self.context_key]
        )

class TabularAnalyticsBoxplot(v.Container):
    def __init__(self, app_context, context_key, **kwargs):
        self.app_context = app_context
        self.context_key = context_key
        super().__init__(
            style_ = "min-width:100%; min-height:100%; display:flex; flex-direction:column;",
            children = [self.context_key]
        )

class TabularAnalyticsDensity(v.Container):
    def __init__(self, app_context, context_key, **kwargs):
        self.app_context = app_context
        self.context_key = context_key
        super().__init__(
            style_ = "min-width:100%; min-height:100%; display:flex; flex-direction:column;",
            children = [self.context_key]
        )

class TabularAnalyticsWordCloud(v.Container):
    def __init__(self, app_context, context_key, **kwargs):
        self.app_context = app_context
        self.context_key = context_key

        self.data = self.app_context.tabular_dataset.current_data

        self.result_togle = "display:none;"

        # column selection
        df_col_names = pd.DataFrame(self.data.columns, columns=['col_names'])
        self.column_selector = get_or_create_class(
            'select_table_card',
            self.app_context,
            context_key = f'{self.context_key}__column_selector', # tabular_analytics_basicinfo__column_selector
            title = '변수 선택',
            data = df_col_names,
            size = {'width':'210px', 'height':'200px'},
            style = 'background-color:#ffffff; border-bottom:1px solid #e0e0e0;',
        )
        # column selection - select all
        select_all_values = [{'index':i} for i in range(len(self.data.columns))]
        self.column_selector.children[1].children[0].selected = select_all_values

        # data range selector
        default = 1000 if len(self.data) / 2  > 1000 else len(self.data) / 2
        self.data_range_selector = get_or_create_class(
            'simple_slider_card',
            self.app_context,
            context_key = f'{self.context_key}__data_range_selector', 
            title = '행 범위',
            range = [1, len(self.data), 1, default],
            size = {'width':'210px', 'height':'90px'},
            style = 'background-color:#ffffff; border-bottom:1px solid #e0e0e0;',
        )

        # 조회하기 버튼
        self.run_button = v.Col(
            children= [
                v.Btn(
                    style_ = "",
                    children = ['조회하기'],
                    rounded = True,
                    depressed = True,
                    dark = True,
                ),
            ],
            style_ = "margin:0; padding:0; display:flex; flex-direction:row; justify-content:flex-end; align-items:center; width:210px;",
        )

        # 영문/한문 Cloud 선택
        self.select_lan = v.Checkbox(
            label = '영문 Cloud', 
            value = False, 
            children = [],
            style_ = "margin:0; padding:0; display:flex;flex-direction:row;justify-content:flex-end"
        
        )


        self.setting_part = get_or_create_class(
            'tabular_data_analytics_options',
            self.app_context,
            context_key = 'tabular_data_analytics__options',
            children = [
                self.column_selector,
                v.Spacer(style_ = "min-height:10px"),
                self.data_range_selector,
                v.Spacer(style_ = "min-height:10px"),
                self.select_lan,
                self.run_button,
            ],
        )

        self.output_part = v.Row(
            class_ = 'tabular_analytics_basicinfo__output_part',
            style_ = "max-height:100%; margin:0; padding:0; background-color:#ffffff; \
                      display:flex, flex-direction:column;",
            children = [self.setting_part],
        )

        super().__init__(
            class_ = self.context_key,
            style_ = "min-width:100%; min-height:100%; padding:0; display:flex; flex-direction:row; background-color:#ffffff00;",
            children = [
                self.output_part
                ],
        )
        def _on_click(item, event, data):
            self.select_lan.value = True

        def _show_wordcloud(item, event, data):


            # 영어 Word Cloud
            self.app_context.progress_linear.active = True
            if self.select_lan.value:
                # (1) column 선택
                selected_cols = self.app_context.tabular_analytics_wcloud__column_selector.children[1].children[0].selected
                if len(selected_cols) == 0:
                    raise Exception('변수를 1개 이상 선택해주세요.')
                selected_cols_to_idx = [col['index'] for col in selected_cols]

                # (2) 데이터 범위 선택
                selected_num_rows = int(self.app_context.tabular_analytics_wcloud__data_range_selector.children[1].children[0].children[0].v_model)

                # (3) 데이터 선택
                self.df = self.app_context.tabular_dataset.current_data.iloc[:selected_num_rows, selected_cols_to_idx]

                # (4) 필요 라이브러리 import
                from wordcloud import WordCloud
                import matplotlib.pyplot as plt
                from collections import Counter
                from PIL import Image
                import numpy as np
                
                # (5) 선택한 column의 값으로 text 만들기    
                selected_cols_name = self.df.columns.to_list()
                text = ""
                for i in range(0, len(selected_cols_name)):
                    text += " ".join(
                        self.df[selected_cols_name[i]].values
                    )
                    text += " "
                
                # (6) Word Cloud 만들기
                wc = WordCloud(width = 400, height = 400, scale = 2.0, max_font_size = 250).generate(text)

                # (7) 이미지 저장
                save_dir = self.app_context.env_values["tmp_dir"]
                data_name = self.app_context.tabular_dataset.current_data_name
                wc.to_file(f"{save_dir}/{data_name}.jpg")
                file = open(f"{save_dir}/{data_name}.jpg", 'rb')
                image = file.read()
                img = w.Image(value = image, fromat = 'jpg')


                self.setting_part.v_model = False
                self.output_part.children = [
                    self.setting_part, 
                    v.Col(
                        children = [img],
                        style_ = "margin:0; padding:0; display:flex; flex-direction:column; max-height:1539px; overflow-y:auto; \
                                padding-top:15px; padding-left:15px",
                    ),
                ]
                self.app_context.progress_linear.active = False
            
            # 한국어 WordCloud
            else:
                self.app_context.progress_linear.active = True
                # (1) column 선택
                selected_cols = self.app_context.tabular_analytics_wcloud__column_selector.children[1].children[0].selected
                if len(selected_cols) == 0:
                    raise Exception('변수를 1개 이상 선택해주세요.')
                selected_cols_to_idx = [col['index'] for col in selected_cols]

                # (2) 데이터 범위 선택
                selected_num_rows = int(self.app_context.tabular_analytics_wcloud__data_range_selector.children[1].children[0].children[0].v_model)

                # (3) 데이터 선택
                self.df = self.app_context.tabular_dataset.current_data.iloc[:selected_num_rows, selected_cols_to_idx]

                # (4) 필요 라이브러리 import
                from wordcloud import WordCloud
                import matplotlib.pyplot as plt
                from collections import Counter
                from konlpy.tag import Okt
                from PIL import Image
                import numpy as np
                # (5) 선택한 column의 값으로 text 만들기
                # selected_cols_name = [col['col_names'] for col in selected_cols]
                selected_cols_name = self.df.columns.to_list()
                text = ""
                for i in range(0, len(selected_cols_name)):
                    # for j in range(0, len(self.df[selected_cols_name[i]])):
                    #     text = text + str(self.df[selected_cols_name[i]][j]) + ','
                    text += " ".join(
                        self.df[selected_cols_name[i]].values
                    )
                    text += " "
                # (6) WordCloud 생성
                okt = Okt()
                nouns = okt.nouns(text)
                words = [n for n in nouns if len(n) >= 1] 
                c = Counter(words)
                wc = WordCloud(font_path = '/usr/share/fonts/NanumGothic-Regular.ttf', width = 400, height = 400, scale = 2.0, max_font_size = 250)
                gen = wc.generate_from_frequencies(c)

                # (7) 이미지 저장
                save_dir = self.app_context.env_values["tmp_dir"]
                data_name = self.app_context.tabular_dataset.current_data_name
                wc.to_file(f"{save_dir}/{data_name}.jpg")
                file = open(f"{save_dir}/{data_name}.jpg", 'rb')
                image = file.read()
                img = w.Image(value = image, fromat = 'jpg')


                self.setting_part.v_model = False
                self.output_part.children = [
                    self.setting_part, 
                    v.Col(
                        children = [img],
                        style_ = "margin:0; padding:0; display:flex; flex-direction:column; max-height:1539px; overflow-y:auto; \
                                padding-top:15px; padding-left:15px",
                    ),
                ]
                self.app_context.progress_linear.active = False



        self.select_lan.on_event('click',_on_click)
        self.run_button.on_event('click',_show_wordcloud)





class TabularAnalyticsDimensionReduction(v.Container):
    def __init__(self, app_context, context_key, **kwargs):
        self.app_context = app_context
        self.context_key = context_key
        super().__init__(
            style_ = "min-width:100%; min-height:100%; display:flex; flex-direction:column;",
            children = [self.context_key]
        )

class TabularAnalyticsClustering(v.Container):
    def __init__(self, app_context, context_key, **kwargs):
        self.app_context = app_context
        self.context_key = context_key
        super().__init__(
            style_ = "min-width:100%; min-height:100%; display:flex; flex-direction:column;",
            children = [self.context_key]
        )

class TabularAnalyticsDataSample(v.Container):
    def __init__(self, app_context, context_key, **kwargs):
        self.app_context = app_context
        self.context_key = context_key

        self.data = self.app_context.tabular_dataset.current_data

        self.result_togle = "display:none;"

        # column selection
        df_col_names = pd.DataFrame(self.data.columns, columns=['col_names'])
        self.column_selector = get_or_create_class(
            'select_table_card',
            self.app_context,
            context_key = f'{self.context_key}__column_selector', # tabular_analytics_basicinfo__column_selector
            title = '변수 선택',
            data = df_col_names,
            size = {'width':'210px', 'height':'200px'},
            style = 'background-color:#ffffff; border-bottom:1px solid #e0e0e0;',
        )
        # column selection - select all
        select_all_values = [{'index':i} for i in range(len(self.data.columns))]
        self.column_selector.children[1].children[0].selected = select_all_values

        # data range selector
        default = 1000 if len(self.data) / 2  > 1000 else len(self.data) / 2
        self.data_range_selector = get_or_create_class(
            'simple_slider_card',
            self.app_context,
            context_key = f'{self.context_key}__data_range_selector', 
            title = '행 범위',
            range = [1, len(self.data), 1, default],
            size = {'width':'210px', 'height':'90px'},
            style = 'background-color:#ffffff; border-bottom:1px solid #e0e0e0;',
        )

        # 조회하기 버튼
        self.run_button = v.Col(
            children= [
                v.Btn(
                    style_ = "",
                    children = ['조회하기'],
                    rounded = True,
                    depressed = True,
                    dark = True,
                ),
            ],
            style_ = "margin:0; padding:0; display:flex; flex-direction:row; justify-content:flex-end; align-items:center; width:210px;",
        )

        self.setting_part = get_or_create_class(
            'tabular_data_analytics_options',
            self.app_context,
            context_key = 'tabular_data_analytics__options',
            children = [
                self.column_selector,
                v.Spacer(style_ = "min-height:10px"),
                self.data_range_selector,
                v.Spacer(style_ = "min-height:10px"),
                self.run_button,
            ],
        )

        self.output_part = v.Row(
            class_ = 'tabular_analytics_basicinfo__output_part',
            style_ = "max-height:100%; margin:0; padding:0; background-color:#ffffff; \
                      display:flex, flex-direction:column;",
            children = [self.setting_part],
        )

        super().__init__(
            class_ = self.context_key,
            style_ = "min-width:100%; min-height:100%; padding:0; display:flex; flex-direction:row; background-color:#ffffff00;",
            children = [
                self.output_part
                ],
        )

        def _show_data_sample(item, event, data):
            self.app_context.progress_linear.active = True

            # (1) Column 선택
            selected_cols = self.app_context.tabular_analytics_datasample__column_selector.children[1].children[0].selected
            if len(selected_cols) == 0:
                raise Exception('변수를 1개 이상 선택해주세요.')
            selected_cols_to_idx = [col['index'] for col in selected_cols]

            # (2) 데이터 범위
            selected_num_rows = int(self.app_context.tabular_analytics_datasample__data_range_selector.children[1].children[0].children[0].v_model)

            # (3) 데이터
            self.df = self.app_context.tabular_dataset.current_data.iloc[:selected_num_rows, selected_cols_to_idx]

            self.output_part.children = [
                v.Col(title = '데이터 상위 10건', children = [self.df.head(10)]),
                v.Col(title = '데이터 하위 10건', children = [self.df.tail(10)]),
                
            ]
            self.app_context.progress_linear.active = False

        self.run_button.on_event('click', _show_data_sample)


