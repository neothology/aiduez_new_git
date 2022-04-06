import ipyvuetify as v
import os
from utils import get_or_create_class, delete_files_in_dir
class TabularBase(v.Container):

    def __init__(self, app_context, context_key, **kwargs):
        self.app_context = app_context
        self.context_key = context_key

        # delete tmp directory contents if exists, else make tmp directory
        tmp_dir = self.app_context.env_values['tmp_dir']
        if os.path.exists(tmp_dir):
            delete_files_in_dir(tmp_dir)
        else:
            os.makedirs(tmp_dir)

        # init workbook
        self.workbook = get_or_create_class('tabular_workbook', self.app_context, 'current_workbook')
        self.workbook.create_new() # tabular, text, image, video, audio, etc.

        # initialize components to view
        work_area_contents = get_or_create_class('sub_area', self.app_context, context_key = 'tabular_contents')

        self.tab_menu = get_or_create_class(
            'tab_menu', 
            self.app_context,  
            context_key = 'tabular_tab_menu',
            tab_props = self.app_context.workflows_list['tabular'],
            target_area = work_area_contents
            )

        # initialize each workflow 
        # tabular_workflow_names = [tab.value for tab in self.tab_menu.tab_menu.children]
        # init_intervals = [10,25,40,10,5]
        # init_progress = 15
        # for i, workflow_name in enumerate(tabular_workflow_names):
        #     _ = get_or_create_class(workflow_name, self.app_context)
        #     init_progress += init_intervals[i]
        #     self.app_context.progress_overlay.update(init_progress)

        # put components into layout
        super().__init__(
            class_ = self.context_key,
            style_ = "min-width:100%; min-height:100%; padding:0px; display:flex; flex-direction:column;",
            children = [
                self.tab_menu, 
                work_area_contents,
                ],
        )

class TabularDataImport_old(v.Container):
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

class TabularDataImport(v.Container):
    def __init__(self, app_context, context_key, **kwargs):
        self.app_context = app_context
        self.context_key = context_key

        self.data_name_list = self.app_context.tabular_dataset.data_name_list

        self.menu_tree = [
            {   
                'icon': 'mdi-laptop',
                'title': 'AIDU에서 가져오기',
                'target': 'tabular_import_aidu',
            },
            {   
                'icon': 'mdi-folder-open-outline',
                'title': 'PC에서 가져오기',
                'target': 'tabular_import_pc',
            },
            {   
                'icon': 'mdi-dns-outline',
                'title': 'EDAP에서 가져오기',
                'target': 'tabular_import_edap',
            },
        ]

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

        # progress bar
        self.progress_bar = v.ProgressLinear(
            indeterminate = True,
            color = 'primary',
        )
        self.progress_bar.active = False

        # sub menu area
        self.work_area_contents_sub_menu = get_or_create_class(
            'sub_menu_area',
            self.app_context,
            style = "min-width:200px; max-width:200px !important; background-color:#e5e5e5; z-index:100;",
        )

        self.sub_menu = get_or_create_class(
            'list_menu_sub',
            self.app_context,
            context_key = 'tabular_data_import__sub_menu',
            menu_tree = self.menu_tree,
        )

        self.work_area_contents_sub_menu.children = [self.sub_menu]

        # sub work area
        self.work_area_contents_sub_area = get_or_create_class(
            'sub_area',
            self.app_context,
            context_key = 'tabular_data_import__sub_contents',
            style = "width:100%; \
                    padding:0; margin:0; background-color:#ffffff00; position:relative; ",
        )

        # activate contents sub area layout


        super().__init__(
            class_ = self.context_key,
            style_ = "min-width:100%; min-height:100%; padding:0; display:flex; flex-direction:column;",
            children = [
                self.top_area,
                self.progress_bar,
                v.Col(
                    style_ = "display:flex; max-height:1599px; flex-direction:row; padding:0; width:1570px; margin:0;",
                    children = [
                        self.work_area_contents_sub_menu,
                        self.work_area_contents_sub_area
                    ],
                )
            ]
        )

class TabularDataAnalytics(v.Container):
    def __init__(self, app_context, context_key, **kwargs):
        self.app_context = app_context
        self.context_key = context_key
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
            style = "min-width:230px; max-width:230px !important; background-color:#e5e5e5;z-index:100;",
        )
                    
        self.sub_menu = get_or_create_class(
            'list_menu_sub',
            self.app_context,
            context_key = 'tabular_data_analytics__sub_menu',
            menu_tree = self.menu_tree,
        )

        self.work_area_contents_sub_menu.children = [self.sub_menu]

        # sub work area
        self.work_area_contents_sub_area = get_or_create_class(
            'sub_area',
            self.app_context,
            context_key = 'tabular_data_analytics__sub_contents',
            style = "width:100%; \
                    padding:0; margin:0; background-color:#ffffff00; position:relative; ",
        )

        super().__init__(
            class_ = self.context_key,
            style_ = "min-width:100%; min-height:100%; padding:0; display:flex; flex-direction:column;",
            children = [
                self.top_area,
                self.progress_bar,
                v.Col(
                    style_ = "display:flex; max-height:1539px; flex-direction:row; padding:0; width:1570px; margin:0;",
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

        self.menu_tree = [
            {   
                'icon': 'mdi-clipboard-text-outline',
                'title': '단일 칼럼 변환',
                'target': 'tabular_data_single_processing',
            },
            {
                'icon': 'mdi-clipboard-text-multiple-outline',
                'title': '복합 칼럼 변환',
                'target': 'tabular_data_multiple_processing',
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
            context_key = 'tabular_data_processing_sub_menu',
            style = "min-width:230px; max-width:230px !important; background-color:#e5e5e5; z-index:100;",
        )

        # vertical tab
        self.processing_sub_menu = get_or_create_class(
            'list_menu_sub',
            app_context=self.app_context,
            context_key='tabular_data_processing__sub_menu',
            menu_tree = self.menu_tree,
        )

        self.work_area_contents_sub_menu.children = [self.processing_sub_menu]

        # sub work area
        self.work_area_contents_sub_area = get_or_create_class(
            'sub_area',
            self.app_context,
            context_key = 'tabular_data_processing__sub_contents',
            style = "width:100%; \
                    padding:0; margin:0; background-color:#ffffff00; position:relative; ",
        )

        super().__init__(
            class_ = self.context_key,
            style_ = "min-width:100%; min-height:100%; padding:0; display:flex; flex-direction:column;",
            children = [
                self.top_area,
                self.progress_bar,
                v.Col(
                    style_ = "display:flex; max-height:1539px; flex-direction:row; padding:0; width:1570px; margin:0;",
                    children = [
                        self.work_area_contents_sub_menu,
                        self.work_area_contents_sub_area
                    ],
                )
            ],
        )

class TabularAITraining(v.Container):

    def __init__(self, app_context, context_key, **kwargs):
        self.app_context = app_context
        self.context_key = context_key
        self.style = {}

        # progress bar
        self.progress_bar = v.ProgressLinear(
            indeterminate = True,
            color = 'primary',
        )
        self.progress_bar.active = False
  

        super().__init__(
            class_ = self.context_key,
            style_ = "min-width:100%; min-height:100%; padding:0; display:flex; flex-direction:column;",
            children = [
                self.progress_bar,
                v.Container()
                ],
        )  

        # self.app_context.tabular_ai_training__training_options.retrieve_training_options()

    def update_contents(self):
        self.data = self.app_context.tabular_dataset.current_data
        self.column_summary.col = self.data[self.data.columns[0]]
        self.column_summary.update_contents()

    def load_contents(self):

        self.progress_bar.active = True

        # data_context
        self.data_context = get_or_create_class(
            'tabular_data_context',
            self.app_context,
        )

        # train button
        self.train_button = get_or_create_class(
            'tabular_train_activator',
            self.app_context,
            context_key = 'tabular_ai_training__train_activator',
            title = '학습하기'
        )

        self.top_area = v.Row(
            children = [
                self.data_context,
                self.train_button,
            ],
            style_ = "margin:0; padding:0; max-height:60px; border-bottom:1px solid #cdcdcd;"
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
            col = self.app_context.tabular_dataset.current_data.iloc[:, 0],
        )     

        self.children = [
                self.top_area,
                v.Spacer(style_ = "min-height:10px; max-height:10px;"),
                self.train_result,
                self.training_options,
                v.Spacer(style_ = "min-height:30px; max-height:30px;"),
                self.column_summary,
                ]
                
        self.progress_bar.active = False


class TabularAIEvaluation(v.Container):
    def __init__(self, app_context, context_key, **kwargs):
        super().__init__(
            style_ = "min-width:100%; min-height:100%;",
            children = []
        )