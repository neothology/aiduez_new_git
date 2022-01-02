import ipyvuetify as v
from utils import get_or_create_class

############### baseline layout ###############

class BackGround(v.Container):
    def __init__(self, app_context, app_config, **kwargs):
        super().__init__(
            class_ = "background",
            style_ = "min-width:100%; max-width:none; \
                height: 900px; margin:0px; padding:0; \
                background-color:#f1f5f9; z-index:0; \
                display:flex; justify-content:center;",
        )
       
class SideNav(v.NavigationDrawer):
    def __init__(self, app_context, app_config, **kwargs):
        super().__init__(
            class_ = "side_nav",
            v_model = False, 
            absolute = True,
            temporary = False,
            permanent = True,
            style_ = "min-width:250px; height:900px; padding:10px; z-index:1000; display:flex; flex-direction:column; background-color:#0f172a", 
        )

    def toggle(self):
        self.v_model = not self.v_model

class TopArea(v.AppBar):
    def __init__(self, app_context, app_config, **kwargs):
        self.side_nav_instance = get_or_create_class('side_nav', app_context, app_config)
        self.nav_icon = v.Container(
            style_ = "min-width:50px; max-width:50px; margin:0; padding:0;",
            children = [v.AppBarNavIcon(style_ = "")]
        )
        self.logo_image = v.Container(
            style_ = "min-width:200px; max-width:200px; margin:0; padding:0;",
            children = [
                v.Img(
                    src = "./assets/images/ico_l_aidu.94ded96e.png", 
                    style_ = "margin-left:5px;",
                    max_width = "100px",
                    max_height = "20px",
                    contain = True,
                )
            ]
        )
        super().__init__(
            class_ = "top_area",
            color = "#ffffff",
            style_ = "height:199px; box-shadow:none; border:0; border-bottom:1px solid #e2e8f0;",
            children = [
                self.nav_icon, 
                self.logo_image,
            ]
        )

        def on_click(widget, event, data):
            self.side_nav_instance.toggle()

        self.nav_icon.on_event('click', on_click)


class WorkArea(v.Container):
    def __init__(self, app_context, app_config, **kwargs):
        self.app_context = app_context
        self.app_config = app_config

        super().__init__(
            class_ = "work_area",
            style_ = "min-width:1700px; max-width:1700px; \
                border-left:1px dashed #cccccc; \
                border-right:1px dashed #cccccc; \
                height: 699px; top:200px; \
                background-color:#f1f5f9; \
                margin:0; padding:0; \
                position:absolute;",
        )

class SubArea(v.Container):
    def __init__(self, app_context, app_config, **kwargs):
        self.app_context = app_context
        self.app_config = app_config

        super().__init__(
            class_ = "sub_area",
            style_ = ""
        )


        

