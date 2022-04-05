import ipyvuetify as v

class BaseDialog(v.Dialog):
    def __init__(
        self,
        v_slots:object = None,
        header_title_main:str = "",
        header_title_sub:str = "",
        header_bottom:object = None,
        body_items:list = [],
        body_size:dict = {},
        body_border_bottom:list = None,
        body_background_color:list = None,
        align:str = '',
        more:bool = False,
        close:bool = True,
        save:bool = False,
        **kwargs,
    ):
        from components.cards import BaseCard
        children = BaseCard(
            header_title_main = header_title_main,
            header_title_sub = header_title_sub,
            header_bottom = header_bottom,
            body_items = body_items,    
            body_size= body_size,
            body_border_bottom = body_border_bottom,
            body_background_color = body_background_color,
            align = align,
            more = more,
            close = close,
            save = save,
            class_ = kwargs.get('class_'),
            app_context = kwargs.get('app_context'),
        )

        super().__init__(
            persistent = True,
            children = [children],
            width = body_size.get('width'),
        )
class SimpleDialog(v.Dialog):
    def __init__(
        self,
        title,
        body,
        buttons,
        size,
        **kwargs,
    ):
        from components.cards import SimpleCard
        children = SimpleCard(
            title = title,
            body = body,
            buttons = buttons,
            size = size,
            **kwargs,
        )

        super().__init__(
            persistent = True,
            children = [children],
            width = size.get('width'),
            style_ = "position:absolute; top:8vh; right:3vh;",
        )

    def show(self):
        self.value = 1
        self.value = 2
