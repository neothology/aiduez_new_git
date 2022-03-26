import ipyvuetify as v
import os
import json
from utils import get_or_create_class
class TabularBase(v.Container):

    def __init__(self, app_context, context_key, **kwargs):
        self.app_context = app_context
        self.context_key = context_key
        self.tmp_workbook_dir = self.app_context.env_values['tmp_workbook_dir']

        # init workbook
        self.workbook = get_or_create_class('tabular_workbook', self.app_context)
        self.workbook.create_new() # tabular, text, image, video, audio, etc.

        # code will be removed: add data from /aihub/data to workbook data list---------
        from os import listdir, path
        import pandas as pd
        from pathlib import Path
        self.data_path_list = [path.join('data', data_name) for data_name in listdir('data')]

        for data_path in sorted(self.data_path_list):
            data = pd.read_csv(data_path, sep = ',', encoding = 'cp949')
            self.workbook.create_new_work(work_name = Path(data_path).stem, data = data)
        # ---------------------------------------------------------------

        # initialize components to view
        work_area_contents = get_or_create_class('sub_area', self.app_context, context_key = 'tabular_contents')

        self.tab_menu = get_or_create_class(
            'tab_menu', 
            self.app_context,  
            tab_props = self.app_context.workflows_list['tabular'],
            context_key = 'tabular_tab_menu',
            target_area = work_area_contents
            )

        # initialize each workflow 

        
        # put components into layout
        super().__init__(
            class_ = self.context_key,
            style_ = "min-width:100%; min-height:100%; padding:0px; display:flex; flex-direction:column;",
            children = [
                self.tab_menu, 
                work_area_contents,
                ],
        )

    def update_workflow_stages(self):
        pass

class TabularDataImport(v.Container):
    def __init__(self, app_context, context_key, **kwargs):
        self.app_context = app_context
        self.context_key = context_key

        self.import_tab = get_or_create_class(
            'tabular_data_import_tab',
            app_context = self.app_context,
            context_key = 'tabular_data_import_tab'
        )
        super().__init__(
            class_ = self.context_key,
            style_ = "min-width:100%; min-height:100%; display:flex; flex-direction:column",
            children = [
                self.import_tab,
                
            ],
        )

class TabularDataAnalytics(v.Container):
    def __init__(self, app_context, context_key, **kwargs):
        self.app_context = app_context
        self.context_key = context_key
        self.style = {}

        self.data = self.app_context.tabular_dataset.current_data
        self.menu_tree = [
            {   
                'icon': 'mdi-file-document-edit-outline',
                'title': '기초정보분석',
                'target': 'tabular_analytics_basicinfo',
            },
            {   
                'icon': 'mdi-file-chart-outline',
                'title': '시각화 분석',
                'sub_menu': [
                    {
                        'icon': 'mdi-scatter-plot-outline',
                        'title': '산점도',
                        'sub_title': 'Scatter',
                        'target': 'tabular_analytics_scatter',
                    },
                    {   
                        'icon': 'mdi-checkerboard',
                        'title': '히트맵',
                        'sub_title': 'Heatmap',
                        'target': 'tabular_analytics_heatmap',
                    },
                    {
                        'icon': 'mdi-checkbox-intermediate',
                        'title': '박스차트',
                        'sub_title': 'Boxplot',
                        'target': 'tabular_analytics_boxplot',
                    },
                    {
                        'icon': 'mdi-chart-bell-curve',
                        'title': '분포차트',
                        'sub_title': 'Densityplot',
                        'target': 'tabular_analytics_density',
                    },
                    {
                        'icon': 'mdi-earth',
                        'title': '한글워드클라우드',
                        'sub_title': 'Korean Words Cloud',
                        'target': 'tabular_analytics_wcloud',
                    },
                ]
            },
            {
                'icon': 'mdi-gesture',
                'title': '비지도학습분석',
                'sub_menu': [
                    {
                        'icon': 'mdi-arrow-collapse-all',
                        'title': '차원축소',
                        'sub_title': 'Dimensionality Reduction',
                        'target': 'tabular_analytics_reduction',
                    },
                    {
                        'icon': 'mdi-gamepad-circle-right',
                        'title': '군집분석',
                        'sub_title': 'Clustering',
                        'target': 'tabular_analytics_clustering',
                    },
                ],
            },
            {
                'icon': 'mdi-text',
                'title': '데이터샘플보기',
                'target': 'tabular_analytics_datasample',
            },

        ]

        # progress bar
        self.progress_bar = v.ProgressLinear(
            indeterminate = True,
            color = 'primary',
        )
        self.progress_bar.active = False

        # top area(data_context, button)
        self.data_context = get_or_create_class(
            'tabular_data_context',
            self.app_context,
        )

        self.top_area = v.Row(
            children = [
                self.data_context
            ],
            style_ = "margin:0; padding:0; max-height:60px; border-bottom:1px solid #cdcdcd;",
        )

        # sub menu area
        self.work_area_contents_sub_menu = get_or_create_class(
            'sub_menu_area',
            self.app_context,
            context_key = 'tabular_analytics_sub_menu',
            style = "width:250px; background-color:#e5e5e5; border: 1px solid #cbcbcb; border-top:0; border-bottom:0;",
        )

        self.sub_menu = get_or_create_class(
            'list_menu_sub',
            self.app_context,
            menu_tree = self.menu_tree,
        )

        self.work_area_contents_sub_menu.children = [self.sub_menu]

        # sub work area
        self.work_area_contents_sub_area = get_or_create_class(
            'sub_area',
            self.app_context,
            context_key = 'tabular_contents_sub',
            style = "width:100%; \
                    padding:0; margin:0; background-color:#ffffff00; position:relative;",
        )

        super().__init__(
            class_ = self.context_key,
            style_ = "min-width:100%; min-height:100%; padding:0; display:flex; flex-direction:column;",
            children = [
                self.top_area,
                self.progress_bar,
                v.Col(
                    style_ = "display:flex; flex-direction:row; padding:0; width:1570px; margin:0;",
                    children = [
                        self.work_area_contents_sub_menu,
                        self.work_area_contents_sub_area
                    ],
                )
            ]
        )

class TabularDataProcessing(v.Container):
    def __init__(self, app_context, context_key, **kwargs):
        self.app_context = app_context
        self.context_key = context_key

         # data_context
        self.data_context = get_or_create_class(
            'tabular_data_context',
            self.app_context,
        )

        # vertical tab
        self.processing_tab = get_or_create_class(
            'tabular_data_processing_tab',
            app_context=self.app_context,
            context_key='tabular_data_processing_tab',
        )

        super().__init__(
            class_ = self.context_key,
            style_ = "min-width:100%; min-height:100%; display:flex; flex-direction:column;",
            children = [
                self.data_context,
                self.processing_tab,
            ],
        )

class TabularAITraining(v.Container):

    def __init__(self, app_context, context_key, **kwargs):
        self.app_context = app_context
        self.context_key = context_key
        self.style = {}

        # data_context
        self.data_context = get_or_create_class(
            'tabular_data_context',
            self.app_context,
        )

        # model
        self.model = get_or_create_class(
            'tabular_model',
            self.app_context,
        )

        # train result
        self.train_result = get_or_create_class(
            'tabular_train_result',
            self.app_context,
            context_key = 'tabular_ai_training__train_result',
            title = '학습 로그',
            size = {'width':'90vw', 'height':'80vh'}, 
        )

        # train button
        self.train_button = get_or_create_class(
            'tabular_train_activator',
            self.app_context,
            context_key = 'tabular_ai_training__train_activator',
            title = '학습하기'
        )

        # training_options
        self.training_options = get_or_create_class(
            'tabular_training_options', 
            self.app_context, 
            context_key = 'tabular_ai_training__training_options',
            title = '학습 Parameter 설정',
        )

        # column summary
        self.column_summary = get_or_create_class(
            'column_summary',
            self.app_context,
            context_key = 'tabular_ai_training__column_summary',
            title = '데이터 요약',
            col = self.app_context.tabular_dataset.current_data.iloc[:, 0]
        )       

        super().__init__(
            class_ = self.context_key,
            style_ = "min-width:100%; min-height:100%; display:flex; flex-direction:column; padding:0;",
            children = [
                self.data_context,
                v.Spacer(style_ = "height:20px"),
                self.train_button ,
                self.train_result,
                v.Spacer(style_ = "height:20px"),
                self.training_options,
                v.Spacer(style_ = "height:30px"),
                self.column_summary,
                v.Spacer(style_ = "height:30px"),
                ],
        )  

        self.app_context.tabular_ai_training__training_options.retrieve_training_options()

    def update_contents(self):
        self.data = self.app_context.tabular_dataset.current_data
        self.column_summary.col = self.data[self.data.columns[0]]
        self.column_summary.update_contents()


class TabularAIEvaluation(v.Container):
    def __init__(self, app_context, context_key, **kwargs):
        super().__init__(
            style_ = "min-width:100%; min-height:100%;",
            children = []
        )