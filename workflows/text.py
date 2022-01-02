import ipyvuetify as v
from utils import get_or_create_class


class TextBase(v.Container):
    navigation_drawer_props = {'temporary':True, 'permanent':False, 'v_model':False}
    def __init__(self, app_context, app_config, **kwargs):
        self.app_context = app_context
        self.app_config = app_config
        
        # initialize components to use
        self.tab_menu = get_or_create_class(
            'tab_menu', 
            self.app_context, self.app_config, 
            tab_props = self.app_config.workflows['text'],
            context_key = 'text_tab_menu',
            )
        self.work_area_contents = get_or_create_class('sub_area', self.app_context, self.app_config, context_key = 'text_contents')

        super().__init__(
            style_ = "min-width:100%; min-height:100%;",
            children = [self.tab_menu, self.work_area_contents],
        )

class TextDataImport(v.Container):
    def __init__(self, app_context, app_config, **kwargs):
        super().__init__(
            style_ = "min-width:100%; min-height:100%;",
            children = []
        )

class TextDataAnalyze(v.Container):
    def __init__(self, app_context, app_config, **kwargs):
        super().__init__(
            style_ = "min-width:100%; min-height:100%;",
            children = []
        )

class TextDataProcessing(v.Container):
    def __init__(self, app_context, app_config, **kwargs):
        super().__init__(
            style_ = "min-width:100%; min-height:100%;",
            children = []
        )

class TextAITraining(v.Container):
    def __init__(self, app_context, app_config, **kwargs):
        super().__init__(
            style_ = "min-width:100%; min-height:100%;",
            children = []
        )

class TextAIEvaluation(v.Container):
    def __init__(self, app_context, app_config, **kwargs):
        super().__init__(
            style_ = "min-width:100%; min-height:100%;",
            children = []
        )
        