import ipyvuetify as v

class ProgressLinear(v.ProgressLinear):
    def __init__(self, context_key, app_context, **kwargs):
        super().__init__(
            indeterminate = True,
            color = 'primary',
            active = False,
            style_ = 'position:absolute; top:200px; z-index:780;',
        )   
