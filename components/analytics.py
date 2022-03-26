from email.policy import default
import pandas as pd
import ipyvuetify as v
from utils import get_or_create_class, get_dataset_stat, get_variable_types

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
            size = {'width':'250px', 'height':'200px'},
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
            range = [0, len(self.data), 1, default],
            size = {'width':'250px', 'height':'90px'},
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
            style_ = "margin:0; padding:0; display:flex; flex-direction:row; justify-content:flex-end; align-items:center; width:250px;",
        )

        self.setting_part = v.NavigationDrawer(
            style_ = "height:1527px; width:266px; padding-top:8px; background-color:#eeeeee;",
            children = [
                v.Col(
                    children = [
                        self.column_selector,
                        v.Spacer(style_ = "min-height:10px"),
                        self.data_range_selector,
                        v.Spacer(style_ = "min-height:10px"),
                        self.run_button,
                        ],
                    style_ = "padding:0; margin:0; display:flex; flex-direction:column; align-items:center",
                )
            ],
            v_model = True,
        )


        output_part_style_off = "max-height:100%; margin:0; background-color:#ffffff; border-top:1px solid #e0e0e0; display:none;"
        output_part_style_on = "max-height:100%; margin:0; background-color:#ffffff; border-top:1px solid #e0e0e0;"
        self.output_part = v.Row(
            style_ = output_part_style_off,
            children = [""],
        )

        super().__init__(
            class_ = self.context_key,
            style_ = "min-width:100%; min-height:100%; padding:0; display:flex; flex-direction:column;",
            children = [
                self.setting_part,
                # v.Spacer(style_ = "max-height:20px"),
                # self.setting_part_2,
                # v.Spacer(style_ = "max-height:8px"),
                # self.output_part
                ],
        )

        def _show_base_info(item, event, data):
            self.app_context.tabular_data_analytics.progress_bar.active = True

            # selected col_names
            selected_cols = self.app_context.tabular_analytics_basicinfo__column_selector.children[1].children[0].selected
            selected_cols_to_idx = [col['index'] for col in selected_cols]

            # data range
            selected_num_rows = int(self.app_context.tabular_analytics_basicinfo__data_range_selector.children[1].children[0].children[0].v_model)

            # data
            self.df = self.app_context.tabular_dataset.current_data.iloc[:selected_num_rows + 1, selected_cols_to_idx]
            
            self.app_context.tabular_data_analytics.progress_bar.active = False

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