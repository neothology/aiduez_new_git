import ipyvuetify as v
from utils import get_or_create_class, set_theme_style

############### baseline layout ###############

class BackGround(v.Container):
    def __init__(self, app_context, context_key, **kwargs):
        self.app_context = app_context
        self.context_key = context_key

        super().__init__(
            class_ = self.context_key,
            style_ = set_theme_style(self.app_context, self.context_key),
        )
       
class SideNav(v.NavigationDrawer):
    def __init__(self, app_context, context_key, **kwargs):
        self.app_context = app_context
        self.context_key = context_key

        super().__init__(
            class_ = self.context_key,
            v_model = False, 
            absolute = True,
            temporary = False,
            permanent = True,
            style_ = set_theme_style(self.app_context, self.context_key ), 
        )

    def toggle(self):
        self.v_model = not self.v_model

class TopArea(v.AppBar):
    def __init__(self, app_context, context_key, **kwargs):
        self.app_context = app_context
        self.context_key = context_key

        self.nav_icon_icon = v.AppBarNavIcon(style_ = set_theme_style(self.app_context, self.context_key, elem='nav_icon_icon', style_type='light'),)
        self.nav_icon = v.Container(
            style_ = set_theme_style(self.app_context, self.context_key, elem='nav_icon', style_type='light'), 
            children = [self.nav_icon_icon],
        )
        self.logo_image = v.Container(
            style_ = set_theme_style(self.app_context, self.context_key, elem='logo_image'),
            children = [
                # v.Img(
                #     src = "./assets/images/ico_l_aidu.94ded96e.png", 
                #     style_ = "margin-left:5px;",
                #     max_width = "100px",
                #     max_height = "20px",
                #     contain = True,
                # )
            ]
        )
        super().__init__(
            class_ = self.context_key,
            style_ = set_theme_style(self.app_context, self.context_key, style_type='light'),
            children = [
                self.nav_icon, 
                self.logo_image,
            ]
        )

        def on_click_toggle(widget, event, data):
            side_nav_instance = get_or_create_class('side_nav', self.app_context, **kwargs)
            side_nav_instance.toggle()

        self.nav_icon.on_event('click', on_click_toggle)

    def change_style(self, style_type):
        # elems = [self, nav_icon, nav_icon_icon ]
        self.style_ = set_theme_style(self.app_context, self.context_key, elem = 'base', style_type=style_type)
        self.nav_icon.style_ = set_theme_style(self.app_context, self.context_key, elem = 'nav_icon', style_type=style_type)
        self.nav_icon_icon.style_ = set_theme_style(self.app_context, self.context_key, elem = 'nav_icon_icon', style_type=style_type)

class WorkArea(v.Container):
    def __init__(self, app_context, context_key, **kwargs):
        self.app_context = app_context
        self.context_key = context_key

        super().__init__(
            class_ = self.context_key,
            style_ = set_theme_style(self.app_context, self.context_key),
        )

class SubArea(v.Container):
    def __init__(self, app_context, context_key, **kwargs):
        self.app_context = app_context
        self.context_key = context_key

        super().__init__(
            class_ = self.context_key,
            style_ = "display:flex; flex-direction:column;" + f'{kwargs.get("style", "")}',
        )

class IndexRow(v.Row):
    def __init__(
        self,
        app_context:object = None,
        context_key:str = "",
        class_: str = "training-options-row",
        index:int = 0,
        **kwargs
        ):
        
        self.index = index
        super().__init__(
            class_ = class_,
            children = kwargs.get('children'),
            style_ = kwargs.get('style_'),
        )