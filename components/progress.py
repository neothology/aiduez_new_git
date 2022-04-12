import ipyvuetify as v

class ProgressLinear(v.ProgressLinear):
    def __init__(self,  app_context, context_key, **kwargs):
        super().__init__(
            indeterminate = True,
            color = 'primary',
            active = False,
            style_ = 'position:absolute; top:200px; z-index:780;',
        )   
        self.app_context = app_context

    def start(self):
        if self.app_context.ignore_progress_linear:
            return
        self.active = True
    
    def stop(self):
        self.active = False