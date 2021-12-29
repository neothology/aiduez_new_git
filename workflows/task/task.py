import ipyvuetify as v

class Task(v.Container):
    def __init__(self, app_context, app_config, **kwargs):
        self.app_context = app_context
        self.app_config = app_config

        super().__init__(
            children = [f'"{self.__class__.__name__}"입니다. 여기에 필요한 화면 및 기능을 구현하세요']
        )
