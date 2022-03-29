import ipyvuetify as v

class BaseOverlay(v.Overlay):
    def __init__(self, context_key, app_context, **kwargs):
        super().__init__(
            value = False,
            children = [
                v.ProgressCircular(
                    indeterminate = True,
                    size = 32,
                ),
            ],
            class_ = kwargs.get('class_'),
            app_context = kwargs.get('app_context'),
            style_ = "z-index:9999;"
        )