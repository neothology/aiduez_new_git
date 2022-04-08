import ipyvuetify as v
import asyncio

class Alert(v.Alert):
    def __init__(
        self,
        app_context:object = None,
        context_key:str = "",
        message:str="message",
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

    def show_and_auto_close(self, message:str="message", alert_type:str="success", seconds:float=3):
        self.message = message
        self.children = [self.message]
        self.type = alert_type

        self.v_model = True
        asyncio.create_task(self.close(seconds))

    async def close(self, seconds):
        await asyncio.sleep(seconds)
        self.v_model = False
