from email.policy import default
from numpy import absolute
import pandas as pd
import ipyvuetify as v
from utils import get_or_create_class
from components.selector import SettingsPartsOptions
from components.cards import SimpleCard, SmallHeaderCard
from components.data_analysis import CreateAnalticsChart
from IPython.display import display

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
            self.app_context.tabular_data_analytics.progress_bar.active = True

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
            self.app_context.tabular_data_analytics.progress_bar.active = False

        self.run_button.on_event('click', _show_base_info)

class TabularAnalyticsScatter(v.Container):
    def __init__(self, app_context, context_key, **kwargs):
        self.app_context = app_context
        self.context_key = context_key

        self.data = self.app_context.tabular_dataset.current_data
        #print(self.data.info())

        # 수치형 컬럼 선택지 조정
        _columnChoices=[]
        for colname in self.data.columns.to_list():
            if self.data[colname].dtype=="int64" or self.data[colname].dtype=="float64":
                _columnChoices.append(colname)

        self.option_widjets=SettingsPartsOptions(
            app_context=self.app_context,
            context_key=self.context_key,
            data=self.data,
            minrowlange=100,
            columnChoices=_columnChoices
        ) 


        # when no class_name in app_context
        self.setting_part = v.NavigationDrawer(
            style_ = "height:1539px; min-width:220px; max-width:220px; padding-top:0px; background-color:#eeeeee;",
            children = [
                v.Col(
                    children = [
                        self.option_widjets.column_selector,
                        v.Spacer(style_ = "min-height:10px"),
                        self.option_widjets.selector_dict['Hue 선택'],
                        v.Spacer(style_ = "min-height:10px"),
                        self.option_widjets.data_range_selector,
                        v.Spacer(style_ = "min-height:10px"),
                        self.option_widjets.run_button,
                    ],
                    style_ = "padding:0; margin:0; display:flex; flex-direction:column; align-items:center",
                )
            ],
        )


        #차트 생성 기능 
        chartmaker= CreateAnalticsChart(self.app_context)
        chart=chartmaker._get_scatter_plot(
            [self.data.columns.to_list()[0]],
            "-",
            100
        )

        self.card_body=v.Row(
            style_='width: 800px; padding-left: 50px; padding-top: 20px;',
            children=[
                v.Card(
                    style_='height: 567px; width: 600px; margin: 0px; padding: 0px; background-color: #F1F5F9; border:hidden; !important; ',
                    children=[
                        v.Card(     
                            style_="align-content: space-around; outline-style: none; max-height: 33px; min-height: 33px; width: 600px; color: #F7FAFC; padding: 0px 0px 0px 0px; \
                            background-color: rgb(248, 250, 252); border-bottom: 1px solid rgb(224, 224, 224); box-shadow: unset; border : none; solid transparent; border-radius: 0px;",
                            outlined=True,            
                            children=[
                                v.CardText(
                                    style_ = "font-size: 0.875rem; color:rgb(100, 116, 139); padding: 6px; ",
                                    children=["차트 보기"]
                                )      
                            ]
                        ),
                        v.Card(
                            outlined=True,
                            style_='max-height: 600px; width: 600px; background-color:#FFFFFF; border-radius: 0px;',       
                            children=[
                                v.List(
                                    children=[chart]
                                )     
                            ]
                        ),
                    ]
                )
            ]
        )

        self.output_part = v.Row(
            class_ = 'tabular_analytics_basicinfo__output_part',
            style_ = "min-width:100%; min-height:100%; padding:0; display:flex; flex-direction:row; background-color:#ffffff00;",
            children = [
                self.setting_part,
                self.card_body
            ],
        )

        #차트 생성 버튼 클릭 조작
        def on_click_with_run_button(widget, event, data):
            chart=chartmaker._get_scatter_plot(
                [ dicElm['col_names'] for dicElm in self.option_widjets.column_selector.select_table.selected ],
                self.option_widjets.selector_dict['Hue 선택'].selected,
                int(self.option_widjets.data_range_selector.body.children[0].children[0].v_model)
            )
            self.app_context.tabular_analytics_scatter.card_body.children[0].children[1].children=[chart]

        # 토글 함수 연동
        self.option_widjets.run_button.on_event('click',on_click_with_run_button)

        super().__init__(
            style_ = "margin:0; padding:0; min-width:100%; min-height:100%; display:flex; flex-direction:column;",
            children = [self.output_part]
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
        super().__init__(
            style_ = "min-width:100%; min-height:100%; display:flex; flex-direction:column;",
            children = [self.context_key]
        )

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
        super().__init__(
            style_ = "min-width:100%; min-height:100%; display:flex; flex-direction:column;",
            children = [self.context_key]
        )