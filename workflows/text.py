import ipyvuetify as v
from utils import get_or_create_class


class TextBase(v.Container):

    def __init__(self, app_context, context_key, **kwargs):
        self.app_context = app_context
        self.context_key = context_key

        self.work_area_contents = get_or_create_class('sub_area', self.app_context, context_key = 'text_contents')
        
        # initialize components to use
        self.tab_menu = get_or_create_class(
            'tab_menu', 
            self.app_context,
            tab_props = self.app_context.workflows_list['text'],
            context_key = 'text_tab_menu',
            target_area = self.work_area_contents,
            )

        super().__init__(
            style_ = "min-width:100%; min-height:100%; padding:0; display:flex; flex-direction:column;",
            children = [self.tab_menu, self.work_area_contents],
        )

class TextDataImport(v.Container):
    def __init__(self, app_context, context_key, **kwargs):
        super().__init__(
            style_ = "min-width:100%; min-height:100%; padding:0; display:flex; flex-direction:column;",
            children = []
        )

class TextDataanalytics(v.Container):
    def __init__(self, app_context, context_key, **kwargs):
        super().__init__(
            style_ = "min-width:100%; min-height:100%; padding:0; display:flex; flex-direction:column;",
            children = []
        )

class TextDataProcessing(v.Container):
    def __init__(self, app_context, context_key, **kwargs):
        super().__init__(
            style_ = "min-width:100%; min-height:100%; padding:0; display:flex; flex-direction:column;",
            children = []
        )

class TextAITraining(v.Container):
    def __init__(self, app_context, context_key, **kwargs):
        super().__init__(
            style_ = "min-width:100%; min-height:100%; padding:0; display:flex; flex-direction:column;",
            children = []
        )

class TextAIEvaluation(v.Container):
    def __init__(self, app_context, context_key, **kwargs):
        super().__init__(
            style_ = "min-width:100%; min-height:100%; padding:0; display:flex; flex-direction:column;",
            children = []
        )
        