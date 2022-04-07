import ipyvuetify as v

class Alert(v.Alert):
    def __init__(
        self,
        app_context:object = None,
        context_key:str = "",
        message:str="",
        alert_type:str="success",
        # v_model:bool=True,
        **kwargs
    ):
        self.message = message
        self.type = alert_type

        super().__init__(
            children = [self.message],
            type = self.type,
            dismissible = True,
            value = True,
            v_model = True,     # this value can open or close alert
            style_ = "position:absolute; top:0; margin:0; width:1570px; z-index:9999;",
            transition="scroll-x-reverse-transition",
        )