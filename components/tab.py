from click import style
import ipyvuetify as v
from utils import get_or_create_class
from pipeline import Pipeline

class BaseTab(v.Tabs):
    def __init__(
        self,
        app_context:object = None,
        context_key:str = "",
        tab_menus:list = [],
        tab_items: list = [],
        vertical:bool = False,
        centered:bool = True,
        ) -> None:
        self.app_context = app_context

        tab_menus = [v.Tab(children=menu) for menu in tab_menus]
        tab_items = [
            v.TabItem(
                class_="pa-3",
                children=[get_or_create_class(item, self.app_context, context_key=item)]) for item in tab_items
        ]

        super().__init__(
            style_ = self.style_,
            class_ = context_key,
            vertical = vertical,
            centered = centered,
            children = tab_menus + tab_items,
        )
