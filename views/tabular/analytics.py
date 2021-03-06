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
    ):
        super().__init__(
            style_ = "height:777px; min-width:220px; max-width:220px; padding-top:8px; background-color:#eeeeee;",
            children = [
                v.Col(
                    children = [],
                    style_ = "padding:0; margin:0; display:flex; flex-direction:column; align-items:center",
                )
            ],
            v_model = False,
            class_ = context_key,
            absolute = True,
            temporary = True,
        )
    
    def nav_open(self):
        self.v_model = True

    def nav_close(self):
        self.v_model = False
    
    def nav_toggle(self):
        self.v_model = not self.v_model

    def update_contents(self, children):
        self.children[0].children = children

class TabularAnalyticsBaseView(v.Container):
    def __init__(self, app_context, context_key, **kwargs):
        self.app_context = app_context
        self.context_key = context_key
        self.target_area = kwargs.get('target_area')

        self.setting_part = get_or_create_class(
            'tabular_data_analytics_options',
            self.app_context,
        )

        self.output_part = v.Row(
            class_ = self.context_key,
            style_ = self.output_part_style,
            children = [self.setting_part],
        )

        super().__init__(
            class_ = self.context_key,
            style_ = "min-width:100%; min-height:100%; padding:0; display:flex; flex-direction:row; background-color:#ffffff00;",
            children = [
                self.output_part
            ],
        )

    def show(self):
        self.setting_part.update_contents(self.setting_part_components)
        self.target_area.children = [self]

class TabularaAnalyticsBasicinfoView(TabularAnalyticsBaseView):
    def __init__(self, app_context, context_key, **kwargs):
        self.app_context = app_context
        self.context_key = context_key
        self.target_area = kwargs.get('target_area')
        self.x_cols = kwargs.get('x_cols')
        self.data_range = kwargs.get('data_range')
        self.selected_data = None
        self.output_part_style = "max-height:100%; margin:0; padding:0px; background-color:#ffffff; \
                    display:flex, flex-direction:column; justify-content:center;"

        # setting area: (1) column selection
        self.column_selector = get_or_create_class(
            'select_table_card',
            self.app_context,
            context_key = f'{self.context_key}__column_selector', # tabular_analytics_scatter_view__column_selector
            title = '?????? ??????',
            data = self.x_cols,
            size = {'width':'210px', 'height':'150px'},
            single_select = False,
        )

        # column selection - select all
        select_all_values = [{'index':i} for i in range(len(self.x_cols))]
        self.column_selector.children[1].children[0].selected = select_all_values

        # setting area: (2) data range selection
        self.data_range_selector = get_or_create_class(
            'simple_slider_card',
            self.app_context,
            context_key = f'{self.context_key}__data_range_selector', 
            title = '??? ??????',
            range = self.data_range,
            size = {'width':'210px', 'height':'90px'},
        )

        # setting area: (4) run button
        self.run_button = v.Col(
            children= [
                v.Btn(
                    style_ = "",
                    children = ['????????????'],
                    depressed = True,
                    dark = True,
                ),
            ],
            style_ = "margin:0; padding:0; display:flex; flex-direction:row; justify-content:flex-end; align-items:center; width:210px;",
        )

        self.setting_part_components = [
            self.column_selector,
            v.Spacer(style_ = "min-height:10px"),
            self.data_range_selector,
            v.Spacer(style_ = "min-height:10px"),
            self.run_button,
        ]

        super().__init__(
            app_context, 
            context_key, 
            target_area = self.target_area
            )

        def _show_result(item, event, data):
            self.app_context.progress_linear.start()

            # selected col_names
            selected_cols = self.column_selector.children[1].children[0].selected
            if len(selected_cols) == 0:
                raise Exception('????????? 1??? ?????? ??????????????????.')
            selected_cols_to_idx = [col['index'] for col in selected_cols]
            
            # data range
            selected_num_rows = int(self.data_range_selector.children[1].children[0].children[0].v_model)

            # data
            self.selected_data = self.app_context.tabular_dataset.current_data.iloc[:selected_num_rows, selected_cols_to_idx]
           
            # make output & show
            self.data_info = get_or_create_class(
                'data_info',
                self.app_context,
                context_key = f'{self.context_key}__data_info', # tabular_analytics_basicinfo__data_info
                data_name = self.app_context.tabular_dataset.current_data_name,
                data = self.selected_data,
                update = True,
            )

            self.columns_info = [
                get_or_create_class(
                    'column_summary_simple',
                    self.app_context,
                    context_key = f'{self.context_key}__column_summary_simple', # tabular_analytics_basicinfo__column_summary_simple
                    title = f'?????????: {col_name}',
                    col = self.selected_data[col_name],
                    update = True,
                ) for col_name in self.selected_data.columns
            ]

            self.setting_part.v_model = False
            self.output_part.children = [
                self.setting_part, 
                v.Col(
                    class_ = "output_part_sub",
                    children = [self.data_info] + self.columns_info,
                    style_ = "margin:0; padding:0; display:flex; flex-direction:column; max-height:777px; overflow-y:auto; \
                              padding-top:15px; padding-left:15px; position:absolute;",
                ),
            ]
            self.app_context.progress_linear.active = False

        self.run_button.on_event('click', _show_result)

class TabularAnalyticsScatterView(TabularAnalyticsBaseView):
    def __init__(self, app_context, context_key, **kwargs):
        self.app_context = app_context
        self.context_key = context_key
        self.target_area = kwargs.get('target_area')
        self.x_cols = kwargs.get('x_cols')
        self.hue_cols = kwargs.get('hue_cols')
        self.data_range = kwargs.get('data_range')
        self.output_part_style = "max-height:100%; margin:0; padding:0px; padding-top:20px; background-color:#ffffff; \
                    display:flex, flex-direction:column; justify-content:center;"

        # setting area: (1) column selection
        self.column_selector = get_or_create_class(
            'select_table_card',
            self.app_context,
            context_key = f'{self.context_key}__column_selector', # tabular_analytics_scatter_view__column_selector
            title = '?????? ??????',
            data = self.x_cols,
            size = {'width':'210px', 'height':'150px'},
            single_select = False,
        )

        # column selection - select all
        select_all_values = [{'index':i} for i in range(len(self.x_cols))]
        self.column_selector.children[1].children[0].selected = select_all_values

        # setting area: (2) hue selection
        self.hue_selector = get_or_create_class(
            'select_table_card',
            self.app_context,
            context_key = f'{self.context_key}__hue_selector', # tabular_analytics_scatter_view__hue_selector
            title = 'Hue ??????',
            data = self.hue_cols,
            size = {'width':'210px', 'height':'150px'},
            single_select = True,
        )

        # setting area: (3) data range selection
        self.data_range_selector = get_or_create_class(
            'simple_slider_card',
            self.app_context,
            context_key = f'{self.context_key}__data_range_selector', 
            title = '??? ??????',
            range = self.data_range,
            size = {'width':'210px', 'height':'90px'},
        )

        # setting area: (4) run button
        self.run_button = v.Col(
            children= [
                v.Btn(
                    style_ = "",
                    children = ['????????????'],
                    depressed = True,
                    dark = True,
                ),
            ],
            style_ = "margin:0; padding:0; display:flex; flex-direction:row; justify-content:flex-end; align-items:center; width:210px;",
        )

        self.setting_part_components = [
            self.column_selector,
            v.Spacer(style_ = "min-height:10px"),
            self.hue_selector,
            v.Spacer(style_ = "min-height:10px"),
            self.data_range_selector,
            v.Spacer(style_ = "min-height:10px"),
            self.run_button
        ]

        super().__init__(
            app_context, 
            context_key, 
            target_area = self.target_area
            )

        def _show_result(item, event, data):
            self.app_context.progress_linear.start()
            import plotly.express as px
            import plotly.graph_objects as go

            self.data = self.app_context.tabular_dataset.current_data

            # selected col_names
            selected_cols = self.column_selector.children[1].children[0].selected
            if len(selected_cols) > 10:
                raise Exception('?????? 10??? ????????? ?????? ????????? ???????????? ???????????????.')
            selected_cols_to_idx = [col['index'] for col in selected_cols]
            selected_col_names = self.x_cols.iloc[selected_cols_to_idx]['col_name'].to_list()

            # selected hue_col_name
            selected_hue = self.hue_selector.children[1].children[0].selected
            selected_hue_name = selected_hue[0]['col_name'] if selected_hue else None

            # data range
            selected_num_rows = int(self.data_range_selector.children[1].children[0].children[0].v_model)

            # data preparation
            data = (self.data
                .pipe(lambda dff: dff.dropna(subset=[selected_hue_name]) if selected_hue_name is not None else dff)
                .pipe(lambda dff: dff.astype({selected_hue_name: 'object'}) if selected_hue_name is not None else dff)
                .head(selected_num_rows))

            # draw plot & show
            fig = go.Figure(px.scatter_matrix(data, dimensions=selected_col_names, color=selected_hue_name, title='Scatter plot'))
            fig.update_layout(width=1000, height=700)

            self.setting_part.v_model = False

            self.output_part.children = [
                self.setting_part, 
                v.Col(
                    children = [go.FigureWidget(fig)],
                    style_ = "",
                )
            ]

            self.app_context.progress_linear.active = False

        self.run_button.on_event('click', _show_result)

class TabularAnalyticsHeatmapView(TabularAnalyticsBaseView):

    def __init__(self, app_context, context_key, **kwargs):
        self.app_context = app_context
        self.context_key = context_key
        self.target_area = kwargs.get('target_area')
        self.x_cols = kwargs.get('x_cols')
        self.data_range = kwargs.get('data_range')
        self.output_part_style = "max-height:100%; margin:0; padding:0px; padding-top:20px; background-color:#ffffff; \
                    display:flex, flex-direction:column; justify-content:center;"

        # setting area: (1) column selection
        self.column_selector = get_or_create_class(
            'select_table_card',
            self.app_context,
            context_key = f'{self.context_key}__column_selector', # tabular_analytics_scatter_view__column_selector
            title = '?????? ??????',
            data = self.x_cols,
            size = {'width':'210px', 'height':'150px'},
            single_select = False,
        )

        # column selection - select 5 cols
        select_all_values = [{'index':i} for i in range(len(self.x_cols))]
        self.column_selector.children[1].children[0].selected = select_all_values[:5]

        # setting area: (2) data range selection
        self.data_range_selector = get_or_create_class(
            'simple_slider_card',
            self.app_context,
            context_key = f'{self.context_key}__data_range_selector', 
            title = '??? ??????',
            range = self.data_range,
            size = {'width':'210px', 'height':'90px'},
        )

        # setting area: (4) run button
        self.run_button = v.Col(
            children= [
                v.Btn(
                    style_ = "",
                    children = ['????????????'],
                    depressed = True,
                    dark = True,
                ),
            ],
            style_ = "margin:0; padding:0; display:flex; flex-direction:row; justify-content:flex-end; align-items:center; width:210px;",
        )

        self.setting_part_components = [
            self.column_selector,
            v.Spacer(style_ = "min-height:10px"),
            self.data_range_selector,
            v.Spacer(style_ = "min-height:10px"),
            self.run_button
        ]

        super().__init__(
            app_context, 
            context_key, 
            target_area = self.target_area
            )

        def _show_result(item, event, data):
            self.app_context.progress_linear.start()
            import plotly.express as px
            import plotly.graph_objects as go

            self.data = self.app_context.tabular_dataset.current_data

            # selected col_names
            selected_cols = self.column_selector.children[1].children[0].selected
            selected_cols_to_idx = [col['index'] for col in selected_cols]
            selected_col_names = self.x_cols.iloc[selected_cols_to_idx]['col_name'].to_list()

            # data range
            selected_num_rows = int(self.data_range_selector.children[1].children[0].children[0].v_model)
            
            labels = selected_col_names
            corr = self.data.head(selected_num_rows).filter(labels).corr().values.tolist()

            fig = go.Figure(go.Heatmap(z=corr, x=labels, y=labels,
                                    colorscale='RdBu', reversescale=True, zmid=0))
            fig.update_layout(title='Heatmap', yaxis=dict(autorange='reversed'), width=1000, height=700)

            self.setting_part.v_model = False
            self.output_part.children = [
                self.setting_part, 
                v.Col(
                    children = [go.FigureWidget(fig)],
                    style_ = "",
                )
            ]

            self.app_context.progress_linear.active = False
        
        self.run_button.on_event('click', _show_result)


class TabularAnalyticsBoxplotView(TabularAnalyticsBaseView):
    def __init__(self, app_context, context_key, **kwargs):
        self.app_context = app_context
        self.context_key = context_key
        self.target_area = kwargs.get('target_area')
        self.x_cols = kwargs.get('x_cols')
        self.y_cols = kwargs.get('y_cols')
        self.hue_cols = kwargs.get('hue_cols')
        self.data_range = kwargs.get('data_range')
        self.output_part_style = "max-height:100%; margin:0; padding:0px; padding-top:20px; background-color:#ffffff; \
                    display:flex, flex-direction:column; justify-content:center;"

        # setting area: (1) column X selection
        self.column_x_selector = get_or_create_class(
            'select_table_card',
            self.app_context,
            context_key = f'{self.context_key}__column_x_selector', # tabular_analytics_scatter_view__column_selector
            title = 'X ?????? ??????',
            data = self.x_cols,
            size = {'width':'210px', 'height':'150px'},
            single_select = True,
            style = 'background-color:#ffffff;',
        )

        self.column_x_selector.children[1].children[0].selected = [{'index':0, 'col_name':self.x_cols.iloc[0]['col_name']}]  # init selected col

        # setting area: (2) column Y selection
        self.column_y_selector = get_or_create_class(
            'select_table_card',
            self.app_context,
            context_key = f'{self.context_key}__column_y_selector', # tabular_analytics_scatter_view__column_selector
            title = 'Y ?????? ??????',
            data = self.y_cols,
            size = {'width':'210px', 'height':'150px'},
            single_select = True,
        )

        self.column_y_selector.children[1].children[0].selected = [{'index':0, 'col_name':self.y_cols.iloc[0]['col_name']}] # init selected col

        # setting area: (3) hue selection
        self.hue_selector = get_or_create_class(
            'select_table_card',
            self.app_context,
            context_key = f'{self.context_key}__hue_selector', # tabular_analytics_scatter_view__hue_selector
            title = 'Hue ??????',
            data = self.hue_cols,
            size = {'width':'210px', 'height':'150px'},
            single_select = True,
        )

        # setting area: (3) data range selection
        self.data_range_selector = get_or_create_class(
            'simple_slider_card',
            self.app_context,
            context_key = f'{self.context_key}__data_range_selector', 
            title = '??? ??????',
            range = self.data_range,
            size = {'width':'210px', 'height':'90px'},
        )

        # setting area: (4) run button
        self.run_button = v.Col(
            children= [
                v.Btn(
                    style_ = "",
                    children = ['????????????'],
                    depressed = True,
                    dark = True,
                ),
            ],
            style_ = "margin:0; padding:0; display:flex; flex-direction:row; justify-content:flex-end; align-items:center; width:210px;",
        )

        self.setting_part_components = [
            self.column_x_selector,
            v.Spacer(style_ = "min-height:10px"),
            self.column_y_selector,
            v.Spacer(style_ = "min-height:10px"),
            self.hue_selector,
            v.Spacer(style_ = "min-height:10px"),
            self.data_range_selector,
            v.Spacer(style_ = "min-height:10px"),
            self.run_button
        ]

        super().__init__(
            app_context, 
            context_key, 
            target_area = self.target_area
            )

        def _show_result(item, event, data):
            self.app_context.progress_linear.start()
            import plotly.express as px
            import plotly.graph_objects as go

            self.data = self.app_context.tabular_dataset.current_data

            # selected x_col_name
            selected_x = self.column_x_selector.children[1].children[0].selected
            selected_x_name = selected_x[0]['col_name'] if selected_x else None

            # selected y_col_name
            selected_y = self.column_y_selector.children[1].children[0].selected
            selected_y_name = selected_y[0]['col_name'] if selected_y else None

            # selected hue_col_name
            selected_hue = self.hue_selector.children[1].children[0].selected
            selected_hue_name = selected_hue[0]['col_name'] if selected_hue else None

            # data range
            selected_num_rows = int(self.data_range_selector.children[1].children[0].children[0].v_model)

            fig = go.FigureWidget(
                self.data
                .pipe(lambda dff: dff.dropna(subset=[selected_hue_name]) if selected_hue_name is not None else dff)
                .head(selected_num_rows)
                .pipe(px.box, x=selected_x_name, y=selected_y_name, color=selected_hue_name, title='Boxplot')
            )

            fig.update_layout(width=1000, height=600)

            self.setting_part.v_model = False
            self.output_part.children = [
                self.setting_part, 
                v.Col(
                    children = [fig],
                    style_ = "",
                )
            ]

            self.app_context.progress_linear.stop()

        self.run_button.on_event('click', _show_result)

class TabularAnalyticsDensityView(TabularAnalyticsBaseView):
    def __init__(self, app_context, context_key, **kwargs):
        self.app_context = app_context
        self.context_key = context_key
        self.target_area = kwargs.get('target_area')
        self.x_cols = kwargs.get('x_cols')
        self.hue_cols = kwargs.get('hue_cols')
        self.data_range = kwargs.get('data_range')
        self.output_part_style = "max-height:100%; margin:0; padding:0px; padding-top:20px; background-color:#ffffff; \
                    display:flex, flex-direction:column; justify-content:center;"

        # setting area: (1) column selection
        self.column_selector = get_or_create_class(
            'select_table_card',
            self.app_context,
            context_key = f'{self.context_key}__column_selector', 
            title = '?????? ??????',
            data = self.x_cols,
            size = {'width':'210px', 'height':'150px'},
            single_select = True,
        )

        self.column_selector.children[1].children[0].selected = [{'index':0, 'col_name':self.x_cols.iloc[0]['col_name']}]  # init selected col
        
        # setting area: (2) hue selection
        self.hue_selector = get_or_create_class(
            'select_table_card',
            self.app_context,
            context_key = f'{self.context_key}__hue_selector', # tabular_analytics_scatter_view__hue_selector
            title = 'Hue ??????',
            data = self.hue_cols,
            size = {'width':'210px', 'height':'150px'},
            single_select = True,
        )

        # setting area: (3) data range selection
        self.data_range_selector = get_or_create_class(
            'simple_slider_card',
            self.app_context,
            context_key = f'{self.context_key}__data_range_selector', 
            title = '??? ??????',
            range = self.data_range,
            size = {'width':'210px', 'height':'90px'},
        )

        # setting area: (4) run button
        self.run_button = v.Col(
            children= [
                v.Btn(
                    style_ = "",
                    children = ['????????????'],
                    depressed = True,
                    dark = True,
                ),
            ],
            style_ = "margin:0; padding:0; display:flex; flex-direction:row; justify-content:flex-end; align-items:center; width:210px;",
        )

        self.setting_part_components = [
            self.column_selector,
            v.Spacer(style_ = "min-height:10px"),
            self.hue_selector,
            v.Spacer(style_ = "min-height:10px"),
            self.data_range_selector,
            v.Spacer(style_ = "min-height:10px"),
            self.run_button
        ]

        super().__init__(
            app_context, 
            context_key, 
            target_area = self.target_area
            )

        def _show_result(item, event, data):
            self.app_context.progress_linear.start()
            import plotly.express as px
            import plotly.graph_objects as go

            self.data = self.app_context.tabular_dataset.current_data

            # selected col_names
            selected_col = self.column_selector.children[1].children[0].selected
            selected_col_name = selected_col[0]['col_name'] if selected_col else None

            # selected hue_col_name
            selected_hue = self.hue_selector.children[1].children[0].selected
            selected_hue_name = selected_hue[0]['col_name'] if selected_hue else None

            # data range
            selected_num_rows = int(self.data_range_selector.children[1].children[0].children[0].v_model)

            # draw plot & show
            color = None if selected_hue_name is None or selected_hue_name == '-' else selected_hue_name
            data = self.data.filter([selected_col_name]) if color is None else self.data.filter([selected_col_name, color]).head(selected_num_rows)

            try:
                fig = px.histogram(data, x=selected_col_name, color=color, hover_data=data.columns)
                fig.update_layout(title_text='Density Plot', width=1000, height=700)

                self.setting_part.v_model = False

                self.output_part.children = [
                    self.setting_part, 
                    v.Col(
                        children = [go.FigureWidget(fig)],
                        style_ = "",
                    )
                ]
            except:
                raise Exception('Hue ????????? ???????????? ?????? ?????? ???????????? ????????????. ?????? Hue ?????? ????????? ?????????.')

            self.app_context.progress_linear.active = False

        self.run_button.on_event('click', _show_result)

class TabularAnalyticsWordCloudView(TabularAnalyticsBaseView):
    def __init__(self, app_context, context_key, **kwargs):
        self.app_context = app_context
        self.context_key = context_key
        self.target_area = kwargs.get('target_area')
        self.x_cols = kwargs.get('x_cols')
        self.hue_cols = kwargs.get('hue_cols')
        self.data_range = kwargs.get('data_range')
        self.output_part_style = "max-height:100%; margin:0; padding:0px; padding-top:20px; background-color:#ffffff; \
                    display:flex, flex-direction:column; justify-content:center;"

        # setting area: (1) column selection
        self.column_selector = get_or_create_class(
            'select_table_card',
            self.app_context,
            context_key = f'{self.context_key}__column_selector', 
            title = '?????? ??????',
            data = self.x_cols,
            size = {'width':'210px', 'height':'150px'},
            single_select = True,
        )

        self.column_selector.children[1].children[0].selected = [{'index':0, 'col_name':self.x_cols.iloc[0]['col_name']}]  # init selected col

        # setting area: (2) language selection
        self.language_selector = get_or_create_class(
            'simple_radio_card',
            self.app_context,
            context_key = f'{self.context_key}__language_selector',
            title = '?????? ??????',
            direction = 'row',
            options = {
                'labels':['??????', '??????'],
                'values':['ko', 'en'],
            },
            size = {'width':'210px', 'height':'90px'},
            style = 'background-color:#ffffff; border-bottom:1px solid #e0e0e0; padding-left:30px; padding-bottom:15px;',
        )

        # setting area: (3) data range selection
        self.data_range_selector = get_or_create_class(
            'simple_slider_card',
            self.app_context,
            context_key = f'{self.context_key}__data_range_selector', 
            title = '??? ??????',
            range = self.data_range,
            size = {'width':'210px', 'height':'90px'},
        )

        # setting area: (4) run button
        self.run_button = v.Col(
            children= [
                v.Btn(
                    style_ = "",
                    children = ['????????????'],
                    depressed = True,
                    dark = True,
                ),
            ],
            style_ = "margin:0; padding:0; display:flex; flex-direction:row; justify-content:flex-end; align-items:center; width:210px;",
        )

        self.setting_part_components = [
            self.column_selector,
            v.Spacer(style_ = "min-height:10px"),
            self.language_selector,
            v.Spacer(style_ = "min-height:10px"),
            self.data_range_selector,
            v.Spacer(style_ = "min-height:10px"),
            self.run_button,
        ]

        super().__init__(
            app_context, 
            context_key, 
            target_area = self.target_area
        )

        def _show_result(item, event, data):
            self.app_context.progress_linear.start()

            self.data = self.app_context.tabular_dataset.current_data

            if self.language_selector.selected_option == 'en':
            # ?????? Word Cloud

                # selected col_name
                selected_col = self.column_selector.children[1].children[0].selected
                selected_col_name = selected_col[0]['col_name'] if selected_col else None

                # data range
                selected_num_rows = int(self.data_range_selector.children[1].children[0].children[0].v_model)

                # ?????? ??????????????? import
                from wordcloud import WordCloud
                import matplotlib.pyplot as plt
                from collections import Counter
                from PIL import Image
                import numpy as np
                
                # ????????? column??? ????????? text ?????????    
                selected_col_data = self.data[selected_col_name].head(selected_num_rows).to_list()
                for i in range(0, len(selected_col_data)):
                    text = " ".join(selected_col_data)
                
                # Word Cloud ?????????
                wc = WordCloud(width = 400, height = 400, scale = 2.0, max_font_size = 250).generate(text)
           
            # ????????? WordCloud
            else:
                # selected col_name
                selected_col = self.column_selector.children[1].children[0].selected
                selected_col_name = selected_col[0]['col_name'] if selected_col else None

                # data range
                selected_num_rows = int(self.data_range_selector.children[1].children[0].children[0].v_model)

                # ?????? ??????????????? import
                from wordcloud import WordCloud
                import matplotlib.pyplot as plt
                from collections import Counter
                from konlpy.tag import Okt
                from PIL import Image
                import numpy as np

        #       # ????????? column??? ????????? text ?????????    
                selected_col_data = self.data[selected_col_name].head(selected_num_rows).to_list()
                for i in range(0, len(selected_col_data)):
                    text = " ".join(selected_col_data)

                # WordCloud ??????
                okt = Okt()
                nouns = okt.nouns(text)
                words = [n for n in nouns if len(n) >= 1] 
                c = Counter(words)
                wc = WordCloud(font_path = '/usr/share/fonts/NanumGothic-Regular.ttf', width = 400, height = 400, scale = 2.0, max_font_size = 250)
                gen = wc.generate_from_frequencies(c)

            # ????????? ??????
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
                    class_ = "output_part_sub",
                    children = [img],
                    style_ = "margin:0; padding:0; display:flex; flex-direction:column; max-height:777px; overflow-y:auto; \
                            padding-top:15px; padding-left:15px",
                )
            ]

            self.app_context.progress_linear.active = False

        self.run_button.on_event('click', _show_result)


class TabularAnalyticsReductionView(TabularAnalyticsBaseView):
    def __init__(self, app_context, context_key, **kwargs):
        self.app_context = app_context
        self.context_key = context_key
        self.target_area = kwargs.get('target_area')
        self.x_cols = kwargs.get('x_cols')
        self.c_cols = kwargs.get('c_cols')
        self.data_range = kwargs.get('data_range')
        self.algorithm_cols = kwargs.get('algorithm_cols')
        self.perplexity_range = kwargs.get('perplexity_range')
        self.output_part_style = "max-height:100%; margin:0; padding:0px; padding-top:20px; background-color:#ffffff; \
                    display:flex, flex-direction:column; justify-content:center;"

        # setting area: (1) algorithm selector
        self.algorithm_selector = get_or_create_class(
            'simple_radio_card',
            self.app_context,
            context_key = f'{self.context_key}__algorithm_selector',
            title = '????????????',
            direction = 'row',
            options = self.algorithm_cols,
            size = {'width':'210px', 'height':'90px'},
            style = 'background-color:#ffffff; border-bottom:1px solid #e0e0e0; padding-left:30px; padding-bottom:15px;',
        )
            
        # setting area: (2) column selection
        self.column_selector = get_or_create_class(
            'select_table_card',
            self.app_context,
            context_key = f'{self.context_key}__column_selector',
            title = '?????? ??????',
            data = self.x_cols,
            size = {'width':'210px', 'height':'150px'},
            single_select = False,
        )
        
        # column selection - select all
        select_all_values = [{'index':i} for i in range(len(self.x_cols))]
        self.column_selector.children[1].children[0].selected = select_all_values

        # setting area: (3) category selection
        self.category_selector = get_or_create_class(
            'select_table_card',
            self.app_context,
            context_key = f'{self.context_key}__category_selector', 
            title = '?????? ??????',
            data = self.c_cols,
            size = {'width':'210px', 'height':'100px'},
            single_select = True,
        )

        # setting area: (4) data range selection
        self.data_range_selector = get_or_create_class(
            'simple_slider_card',
            self.app_context,
            context_key = f'{self.context_key}__data_range_selector', 
            title = '??? ??????',
            range = self.data_range,
            size = {'width':'210px', 'height':'90px'},
        )

        # setting area: (5) perplexity slider
        self.perplexity_selector = get_or_create_class(
            'simple_slider_card',
            self.app_context,
            context_key = f'{self.context_key}__perplexity_selector', 
            title = 'Perplexity',
            range = self.perplexity_range,
            size = {'width':'210px', 'height':'90px'},
        )
        
        self.perplexity_selector_area = v.Row(
            children = [],
            style_  = "margin:0; padding:0; display:flex; flex-direction:column; justify-content:center; align-items:center; \
                     width:210px;",
        )

        # setting area: (6) run button
        self.run_button = v.Col(
            children= [
                v.Btn(
                    style_ = "",
                    children = ['????????????'],
                    depressed = True,
                    dark = True,
                ),
            ],
            style_ = "margin:0; padding:0; display:flex; flex-direction:row; justify-content:flex-end; align-items:center; width:210px;",
        )

        self.setting_part_components = [
            self.algorithm_selector,
            v.Spacer(style_ = "min-height:10px"),
            self.column_selector,
            v.Spacer(style_ = "min-height:10px"),
            self.category_selector,
            v.Spacer(style_ = "min-height:10px"),
            self.data_range_selector,
            v.Spacer(style_ = "min-height:10px"),
            self.perplexity_selector_area,
            self.run_button
        ]

        super().__init__(
            app_context, 
            context_key, 
            target_area = self.target_area
        )

        def _show_conditional_option(item, event, data):
            if item.v_model == 't_sne':
                self.perplexity_selector_area.children = [self.perplexity_selector, v.Spacer(style_ = "min-height:10px")]
            else:
                self.perplexity_selector_area.children = []

        def _show_result(item, event, data):
            self.app_context.progress_linear.start()

            # selected cols
            selected_cols = self.column_selector.children[1].children[0].selected
            selected_cols_to_idx = [col['index'] for col in selected_cols]
            selected_col_names = self.x_cols.iloc[selected_cols_to_idx]['col_name'].to_list()
            if len(selected_col_names) < 3:
                raise Exception('?????? 3??? ????????? ????????? ????????? ?????????.')

            # selected category
            selected_category = self.category_selector.children[1].children[0].selected
            selected_category_name = selected_category[0]['col_name'] if selected_category else None

            # selected data range
            selected_num_rows = int(self.data_range_selector.children[1].children[0].children[0].v_model)

            selected_algorithm = self.algorithm_selector.children[1].children[0].children[0].v_model

            # selected perplexity
            selected_perplexity = self.perplexity_selector.children[1].children[0].children[0].v_model

            # draw plot & show
            from sklearn.manifold import TSNE
            from sklearn.decomposition import PCA
            import plotly.express as px
            from plotly.offline import iplot
            import plotly.graph_objects as go

            self.data = self.app_context.tabular_dataset.current_data

            selected_col_names_for_projection = selected_col_names + ([selected_category_name] if selected_category_name else [])
            data = self.data.filter(selected_col_names_for_projection).dropna().head(selected_num_rows)

            options = {'n_components':2, 'random_state':0}
            if selected_algorithm == 'pca':
                chart_title = "PCA ????????????(Dimensionality Reduction)"
                model = PCA(**options)
            else:
                chart_title = "t-SNE ????????????(Dimensionality Reduction)"
                options['perplexity'] = selected_perplexity
                model = TSNE(**options)

            projections = model.fit_transform(data.filter(selected_col_names))

            if selected_category_name:
                color = data[selected_category_name].astype('category')
                labels = {'color':color.name}
            else:
                color = labels = None

            fig = px.scatter(projections, x=0, y=1, color=color, labels=labels, title=chart_title)
            fig.update_layout(width=1000, height=700)

            self.setting_part.v_model = False
            self.output_part.children = [
                self.setting_part,   
                v.Col(
                    children = [go.FigureWidget(fig)],
                    style_ = "",
                )
            ]

            self.app_context.progress_linear.stop()

        self.algorithm_selector.children[1].children[0].children[0].on_event('change', _show_conditional_option)
        self.run_button.on_event('click', _show_result)


class TabularAnalyticsClusteringView(TabularAnalyticsBaseView):
    def __init__(self, app_context, context_key, **kwargs):
        self.app_context = app_context
        self.context_key = context_key
        self.target_area = kwargs.get('target_area')
        self.x_cols = kwargs.get('x_cols')
        self.data_range = kwargs.get('data_range')
        self.algorithm_cols = kwargs.get('algorithm_cols')
        self.clustering_range = kwargs.get('clustering_range')
        self.output_part_style = "max-height:100%; margin:0; padding:0px; padding-top:20px; background-color:#ffffff; \
                    display:flex, flex-direction:column; justify-content:center;"

        # setting area: (1) algorithm selector
        self.algorithm_selector = get_or_create_class(
            'simple_radio_card',
            self.app_context,
            context_key = f'{self.context_key}__algorithm_selector',
            title = '????????????',
            direction = 'row',
            options = self.algorithm_cols,
            size = {'width':'210px', 'height':'90px'},
            style = 'background-color:#ffffff; border-bottom:1px solid #e0e0e0; padding-left:7px; padding-bottom:15px;',
        )
            
        # setting area: (2) column selection
        self.column_selector = get_or_create_class(
            'select_table_card',
            self.app_context,
            context_key = f'{self.context_key}__column_selector',
            title = '?????? ??????',
            data = self.x_cols,
            size = {'width':'210px', 'height':'150px'},
            single_select = False,
        )
        
        # column selection - select all
        select_all_values = [{'index':i} for i in range(len(self.x_cols))]
        self.column_selector.children[1].children[0].selected = select_all_values

        # setting area: (3) clustering range selection
        self.clustering_range_selector = get_or_create_class(
            'simple_slider_card',
            self.app_context,
            context_key = f'{self.context_key}__clustering_range_selector', 
            title = '?????? ??????',
            range = self.clustering_range,
            size = {'width':'210px', 'height':'90px'},
        )

        # setting area: (4) elbow resurt check
        self.elbow_resurt_check = v.Row(
            style_ = "flex-direction:column;",
            children = [
                v.Checkbox(
                    v_model = False,
                    hide_details = True,
                    label = 'Elbow ???????????? ??????',
                    style_ = 'margin:0; padding-left:5px;',
                ),
                v.Col(
                    style_ = "width:210px; height:30px; padding: 5px; padding-left:30px; color:rgba(0, 0, 0, 0.6);",
                    children = ['(???????????? ????????? ???????????????)']
                )

            ]
        )

        # setting area: (5) data range selection
        self.data_range_selector = get_or_create_class(
            'simple_slider_card',
            self.app_context,
            context_key = f'{self.context_key}__data_range_selector', 
            title = '??? ??????',
            range = self.data_range,
            size = {'width':'210px', 'height':'90px'},
        )

        # setting area: (6) run button
        self.run_button = v.Col(
            children= [
                v.Btn(
                    style_ = "",
                    children = ['????????????'],
                    depressed = True,
                    dark = True,
                ),
            ],
            style_ = "margin:0; padding:0; display:flex; flex-direction:row; justify-content:flex-end; align-items:center; width:210px;",
        )

        self.setting_part_components = [
            self.algorithm_selector,
            v.Spacer(style_ = "min-height:10px"),
            self.column_selector,
            v.Spacer(style_ = "min-height:10px"),
            self.clustering_range_selector,
            v.Spacer(style_ = "min-height:10px"),
            self.data_range_selector,
            v.Spacer(style_ = "min-height:10px"),
            self.elbow_resurt_check,
            v.Spacer(style_ = "min-height:10px"),
            self.run_button
        ]

        super().__init__(
            app_context, 
            context_key, 
            target_area = self.target_area
        )

        def _show_result(item, event, data):
            self.app_context.progress_linear.start()

            # selected cols
            selected_cols = self.column_selector.children[1].children[0].selected
            selected_cols_to_idx = [col['index'] for col in selected_cols]
            selected_col_names = self.x_cols.iloc[selected_cols_to_idx]['col_name'].to_list()
            if len(selected_col_names) < 3:
                raise Exception('?????? 3??? ????????? ????????? ????????? ?????????.')

            # clustering range
            selected_clustering_range = int(self.clustering_range_selector.children[1].children[0].children[0].v_model)

            # selected data range
            selected_num_rows = int(self.data_range_selector.children[1].children[0].children[0].v_model)

            selected_algorithm = self.algorithm_selector.children[1].children[0].children[0].v_model

            # elbow resurt check
            elbow_result_check = self.elbow_resurt_check.children[0].v_model

            # draw plot & show
            from sklearn.preprocessing import MinMaxScaler
            from sklearn.cluster import KMeans
            from sklearn.cluster import AgglomerativeClustering
            from sklearn.decomposition import PCA
            from sklearn.impute import SimpleImputer
            import plotly.express as px
            import plotly.graph_objects as go
            import numpy as np

            self.data = self.app_context.tabular_dataset.current_data

            scaler = MinMaxScaler(feature_range=(0, 1))
            imp = SimpleImputer(missing_values=np.nan, strategy='mean')

            target_data = self.data.head(min(self.data.shape[0], selected_num_rows))
            imputed = imp.fit_transform(target_data.filter(selected_col_names))
            scaled = scaler.fit_transform(imputed)

            if selected_algorithm == 'km':
                model = KMeans(n_clusters=selected_clustering_range, algorithm='auto')
                chart_title = f"k-Means ??????(Clustering) ?????????"
            elif selected_algorithm == 'hier':
                model = AgglomerativeClustering(n_clusters=selected_clustering_range, linkage='ward')
                chart_title = f"????????????(Agglomerative Clustering) ?????????"

            predict = pd.DataFrame(model.fit_predict(scaled))
            predict.columns=['cluster']

            color = predict['cluster'].astype('category')
            labels = {'color':color.name}
            options = {'n_components':2, 'random_state':0}

            projector = PCA(**options)
            projections = projector.fit_transform(scaled)

            hover_cols = target_data.drop(columns=['color']).columns.values if 'color' in target_data.columns.values else target_data.columns.values
            target_data['PC1'] = projections[:, 0]
            target_data['PC2'] = projections[:, 1]

            fig = px.scatter(projections, x=0, y=1, color=color, labels=labels, title=chart_title)
            fig.update_layout(width=1000, height=700)

            self.setting_part.v_model = False
            self.output_part.children = [
                self.setting_part,   
                v.Col(
                    children = [go.FigureWidget(fig)],
                    style_ = "",
                ),
            ]

            self.app_context.progress_linear.stop()

        self.run_button.on_event('click', _show_result)

class TabularAnalyticsDataSampleView(TabularAnalyticsBaseView):
    def __init__(self, app_context, context_key, **kwargs):
        self.app_context = app_context
        self.context_key = context_key
        self.target_area = kwargs.get('target_area')
        self.x_cols = kwargs.get('x_cols')
        self.data_range = kwargs.get('data_range')
        self.selected_data = None
        self.output_part_style = "max-height:100%; margin:0; padding:0px; background-color:#ffffff; \
                    display:flex, flex-direction:column; justify-content:center;"

        # setting area: (1) column selection
        self.column_selector = get_or_create_class(
            'select_table_card',
            self.app_context,
            context_key = f'{self.context_key}__column_selector', 
            title = '?????? ??????',
            data = self.x_cols,
            size = {'width':'210px', 'height':'150px'},
            single_select = False,
        )

        # column selection - select all
        select_all_values = [{'index':i} for i in range(len(self.x_cols))]
        self.column_selector.children[1].children[0].selected = select_all_values

        # setting area: (2) data range selection
        self.data_range_selector = get_or_create_class(
            'simple_slider_card',
            self.app_context,
            context_key = f'{self.context_key}__data_range_selector', 
            title = '??? ??????',
            range = self.data_range,
            size = {'width':'210px', 'height':'90px'},
        )

        # setting area: (3) run button
        self.run_button = v.Col(
            children= [
                v.Btn(
                    style_ = "",
                    children = ['????????????'],
                    depressed = True,
                    dark = True,
                ),
            ],
            style_ = "margin:0; padding:0; display:flex; flex-direction:row; justify-content:flex-end; align-items:center; width:210px;",
        )

        self.setting_part_components = [
            self.column_selector,
            v.Spacer(style_ = "min-height:10px"),
            self.data_range_selector,
            v.Spacer(style_ = "min-height:10px"),
            self.run_button,
        ]

        super().__init__(
            app_context, 
            context_key, 
            target_area = self.target_area
            )

        self.data_head = self.data_tail = None
        def _show_result(item, event, data):
            self.app_context.progress_linear.start()

            # selected col_names
            selected_cols = self.column_selector.children[1].children[0].selected
            if len(selected_cols) == 0:
                raise Exception('????????? 1??? ?????? ??????????????????.')
            selected_cols_to_idx = [col['index'] for col in selected_cols]
            
            # data range
            selected_num_rows = int(self.data_range_selector.children[1].children[0].children[0].v_model)

            # data
            self.selected_data = self.app_context.tabular_dataset.current_data.iloc[:selected_num_rows, selected_cols_to_idx]
           
            # make output & show
            self.data_head = get_or_create_class(
                'datatable',
                self.app_context,
                context_key = f'{self.context_key}__sample_data_header', # tabular_analytics_basicinfo__data_info
                data = self.selected_data.head(10),
                title = 'First Rows',
                update = True,
            )

            self.data_tail = get_or_create_class(
                'datatable',
                self.app_context,
                context_key = f'{self.context_key}__sample_data_header', # tabular_analytics_basicinfo__data_info
                data = self.selected_data.tail(10),
                title = 'Last Rows',
                update = True,
            )

            self.setting_part.v_model = False
            self.output_part.children = [
                self.setting_part, 
                v.Col(
                    class_ = "output_part_sub",
                    children = [self.data_head, v.Spacer(style_ = 'min-height:15px; max-height: 15px'), self.data_tail],
                    style_ = "margin:0; padding:0; display:flex; flex-direction:column; max-height:777px; overflow-y:auto; \
                              padding-top:15px; padding-left:15px; padding-right:15px; position:absolute;",
                ),
            ]
            self.app_context.progress_linear.active = False

        self.run_button.on_event('click', _show_result)


