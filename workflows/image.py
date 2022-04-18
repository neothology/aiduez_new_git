import ipyvuetify as v
from utils import get_or_create_class


class ImageBase(v.Container):

    def __init__(self, app_context, context_key, **kwargs):
        self.app_context = app_context
        self.context_key = context_key

    def create_new(self):
        pass

class ImageDataImport(v.Container):
    def __init__(self, app_context, context_key, **kwargs):
        super().__init__(
            style_ = "min-width:100%; min-height:100%; padding:0; display:flex; flex-direction:column;",
            children = []
        )

class ImageDataanalytics(v.Container):
    def __init__(self, app_context, context_key, **kwargs):
        super().__init__(
            style_ = "min-width:100%; min-height:100%; padding:0; display:flex; flex-direction:column;",
            children = []
        )

class ImageDataProcessing(v.Container):
    def __init__(self, app_context, context_key, **kwargs):
        super().__init__(
            style_ = "min-width:100%; min-height:100%; padding:0; display:flex; flex-direction:column;",
            children = []
        )

class ImageAITraining(v.Container):
    def __init__(self, app_context, context_key, **kwargs):
        super().__init__(
            style_ = "min-width:100%; min-height:100%; padding:0; display:flex; flex-direction:column;",
            children = []
        )

class ImageAIEvaluation(v.Container):
    def __init__(self, app_context, context_key, **kwargs):
        super().__init__(
            style_ = "min-width:100%; min-height:100%; padding:0; display:flex; flex-direction:column;",
            children = []
        )