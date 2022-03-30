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
        )

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
            class_ = kwargs.get('class_'),
            app_context = kwargs.get('app_context'),
        )

    def start(self):
        self.value = True

    def update(self, value):
        self.children[0].value = value
       
    def finish(self):
        self.value = False
        self.children[0].value = 0