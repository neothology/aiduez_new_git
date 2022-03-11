import ipyvuetify as v
from utils import get_or_create_class

class TabularBase(v.Container):

    def __init__(self, app_context, context_key, **kwargs):
        self.app_context = app_context
        self.context_key = context_key

        # initialize components to use
        self.tab_menu = get_or_create_class(
            'tab_menu', 
            self.app_context,  
            tab_props = self.app_context.workflows_list['tabular'],
            context_key = 'tabular_tab_menu',
            )
        self.work_area_contents = get_or_create_class('sub_area', self.app_context, context_key = 'tabular_contents')

        super().__init__(
            style_ = "min-width:100%; min-height:100%;",
            children = [
                self.tab_menu, 
                self.work_area_contents,
                ],
        )

class TabularDataImport(v.Container):
    def __init__(self, app_context, context_key, **kwargs):
        super().__init__(
            style_ = "min-width:100%; min-height:100%;",
            children = []
        )

class TabularDataAnalyze(v.Container):
    def __init__(self, app_context, context_key, **kwargs):
        super().__init__(
            style_ = "min-width:100%; min-height:100%;",
            children = ["안녕하세요"]
        )

class TabularDataProcessing(v.Container):
    def __init__(self, app_context, context_key, **kwargs):
        self.app_context = app_context
        self.context_key = context_key
        self.data = app_context.current_data

        # code_will_be_removed: load test data for tabular modeling
        self.app_context.current_data_name = ('titanic_train')
        import pandas as pd
        self.app_context.current_data = pd.read_csv('data/titanic_train.csv')

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
                self.processing_tab,
            ],
        )

class TabularAITraining(v.Container):
    def __init__(self, app_context, context_key, **kwargs):
        self.app_context = app_context
        self.context_key = context_key
        self.data = app_context.current_data
        self.style = {}

        # code_will_be_removed: load test data for tabular modeling
        self.app_context.current_data_name = ('titanic_train')
        import pandas as pd
        self.app_context.current_data = pd.read_csv('data/titanic_train.csv')

        # train button
        self.train_button = get_or_create_class(
            'tabular_train_activator',
            self.app_context,
            title = '학습하기'
        )

        # train result
        self.train_result = get_or_create_class(
            'tabular_train_result',
            self.app_context,
            context_key = 'tabular_ai_training__train_result',
            title = '학습 로그',
            size = {'width':'90vw', 'height':'80vh'}, 
        )

        # modeling_options
        self.modeling_options = get_or_create_class(
            'tabular_modeling_options', 
            self.app_context, 
            context_key = 'tabular_ai_training__modeling_options',
            title = '데이터 설정',
        )

        # column summary
        initial_column_name = self.data.columns[0]
        self.column_summary = get_or_create_class(
            'column_summary',
            self.app_context,
            context_key = 'tabular_ai_training__column_summary',
            title = '데이터 요약',
            col = self.data[initial_column_name],
        )       

        super().__init__(
            class_ = self.context_key,
            style_ = "min-width:100%; min-height:100%; display:flex; flex-direction:column;",
            children = [
                self.train_button ,
                self.train_result,
                v.Spacer(style_ = "height:20px"),
                self.modeling_options,
                v.Spacer(style_ = "height:30px"),
                self.column_summary,
                v.Spacer(style_ = "height:30px"),
                ],
        )   
      
class TabularAIEvaluation(v.Container):
    def __init__(self, app_context, context_key, **kwargs):
        super().__init__(
            style_ = "min-width:100%; min-height:100%;",
            children = []
        )