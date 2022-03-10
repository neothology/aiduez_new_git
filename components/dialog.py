import ipyvuetify as v
from components.cards import BaseCard, SimpleCard

class BaseDialog(v.Dialog):
    def __init__(
        self,
        v_slots:object = None,
        header_title:str = "",
        header_bottom = None,
        body_items:list = [],
        body_size:dict = {},
        body_border_bottom:list = None,
        body_background_color:list = None,
        align:str = '',
        more:bool = False,
        close:bool = True,
        **kwargs,
    ):

        children = BaseCard(
            header_title = header_title,
            header_bottom = header_bottom,
            body_items = body_items,    
            body_size= body_size,
            body_border_bottom = body_border_bottom,
            body_background_color = body_background_color,
            align = align,
            more = more,
            close = close,
            class_ = kwargs.get('class_'),
            app_context = kwargs.get('app_context'),
            selector = kwargs.get('selector'),
        )

        super().__init__(
            persistent = True,
            children = [children],
            width = body_size.get('width'),

        )
