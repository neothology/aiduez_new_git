import ipyvuetify as v
from utils import get_or_create_class


class VideoBase(v.Container):

    def __init__(self, app_context, context_key, **kwargs):
        self.app_context = app_context
        self.context_key = context_key

    def create_new(self):
        pass

class VideoDataImport(v.Container):
    def __init__(self, app_context, context_key, **kwargs):
        super().__init__(
            style_ = "min-width:100%; min-height:100%; padding:0; display:flex; flex-direction:column;",
            children = []
        )

class VideoDataanalytics(v.Container):
    def __init__(self, app_context, context_key, **kwargs):
        super().__init__(
            style_ = "min-width:100%; min-height:100%; padding:0; display:flex; flex-direction:column;",
            children = []
        )

class VideoDataProcessing(v.Container):
    def __init__(self, app_context, context_key, **kwargs):
        super().__init__(
            style_ = "min-width:100%; min-height:100%; padding:0; display:flex; flex-direction:column;",
            children = []
        )

class VideoAITraining(v.Container):
    def __init__(self, app_context, context_key, **kwargs):
        super().__init__(
            style_ = "min-width:100%; min-height:100%; padding:0; display:flex; flex-direction:column;",
            children = []
        )

class VideoAIEvaluation(v.Container):
    def __init__(self, app_context, context_key,  **kwargs):
        super().__init__(
            style_ = "min-width:100%; min-height:100%; padding:0; display:flex; flex-direction:column;",
            children = []
        )