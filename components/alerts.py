import ipyvuetify as v

class Alert(v.Alert):
    def __init__(
        self,
        app_context:object,
        context_key:str,
    ):

        super().__init__(
            v_model = False,     # this value can open or close alert
            border = "left",
            dismissible = True,
            dense = True,
            style_ = "position:absolute; top:0; left:0; margin:0; width:100%; z-index:9999; border-radius: 0 0 12px 12px;",
            transition="scroll-x-reverse-transition",
        )

    def error(self, message):
        self.v_model = False
        self.children = [message]
        self.type = 'error'
        self.v_model = True

    def release(self):
        self.v_model = False
