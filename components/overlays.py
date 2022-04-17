import ipyvuetify as v

class BaseOverlay(v.Overlay):
    def __init__(self, app_context, context_key, **kwargs):
        self.app_context = app_context
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
            z_index=1000,
        )

    def start(self):
        self.app_context.ignore_progress_linear = True
        self.value = True

    def stop(self):
        self.value = False
        self.app_context.ignore_progress_linear = False

class ProgressOverlay(v.Overlay):
    def __init__(self, context_key, app_context, **kwargs):
        super().__init__(
            value = False,
            children = [
                v.ProgressCircular(
                    rotate = -90,
                    size = 50,
                    width = 8,
                    value = 0,
                    children = [],
                ),
            ],
            z_index=1000,
        )

    def start(self):
        self.value = True

    def update(self, value):
        self.children[0].value = value
       
    def stop(self):
        self.value = False
        self.children[0].value = 0