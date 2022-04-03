import ipyvuetify as v

class Alert(v.Alert):
    def __init__(
        self,
        app_context:object = None,
        context_key:str = "",
        **kwargs
    ):
        self.message = "'message'"
        self.type = "success"

        super().__init__(
            children = [self.message],
            type = self.type,
            dismissible = True,
            value = True,
            style_ = "position:absolute; top:0; margin:0; width:1570px; z-index:9999;",
            transition="scroll-x-reverse-transition",
        )


