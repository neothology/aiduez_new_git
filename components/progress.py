import ipyvuetify as v

class ProgressLinear(v.ProgressLinear):
    def __init__(self,  app_context, context_key, **kwargs):
        self.app_context = app_context
        self.style = kwargs.get('style', '')
        
        super().__init__(
            indeterminate = True,
            color = 'primary',
            active = False,
            style_ = self.style,
        )   

    def start(self):
        if self.app_context.ignore_progress_linear:
            return
        self.active = True
    
    def stop(self):
        self.active = False