import ipyvuetify as v
from ipyvuetify.generated.Label import Label

############### left side menu ###############

class Select:
    def __init__(self, app_config, app_context, **kwargs):
        self.app_config = app_config
        self.app_context = app_context
        self.kwargs = kwargs

        self.container = v.Select(
            label = self.kwargs.get('label'),
            items = self.kwargs.get('items'),
            color = self.kwargs.get('color'),
            style_ = self.kwargs.get('style_'),
            class_ = self.kwargs.get('class_'),
        )
        
    def render(self):
        return self.container
