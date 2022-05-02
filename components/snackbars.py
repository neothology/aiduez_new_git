from operator import index
import ipyvuetify as v

class SnackBar(v.Snackbar):
    def __init__(
        self,
        app_context:object,
        context_key:str,
    ):

        super().__init__(
            v_model = False,     # this value can open or close alert
            style_ = "z-index:1001;"
        )

    def error(self, message):
        self.v_model = False
        self.children = [
            v.Icon(
                class_="material-icons", 
                children="warning", 
                color="white", 
                style_ = "margin-right:10px"
            ),
            message
        ]
        self.color = "error"
        self.timeout = 3000
        self.v_model = True

    def success(self, message):
        self.v_model = False
        self.children = [
            v.Icon(
                class_="material-icons",
                children="check_circle",
                color="white",
                style_ = "margin-right:10px"
            ),
            message
        ]
        self.color = "info"
        self.timeout = 3000
        self.v_model = True

    def release(self):
        self.v_model = False
