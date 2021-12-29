import ipyvuetify as v
from utils import get_or_create_class

class ListMenu(v.List):

    def __init__(self, app_context, app_config, **kwargs):
        self.app_context = app_context
        self.app_config = app_config
        self.menu_to_work_area = [] # to collect menus to be clicked

        def _make_sub_menu(sub_items: list) -> list:

            sub_menu = [v.ListItemGroup(
                class_ = "",
                style_ = "",
                children = [v.ListItem(
                    class_ = item["workflow_class_name"],
                    style_ = "padding-left:32px;",
                    active = False,
                    ripple = False,
                    children = [
                        v.ListItemIcon(
                            style_ = "min-width:30px; max-width:30px; margin:0; padding:0; align-self:center;",
                            children = [v.Icon(
                                style_ = "color:#ffffff; font-size:20px;",
                                children = [item['icon']])]
                        ),
                        v.ListItemContent(
                            style_ = "padding-left:15px; color:#ffffff;",
                            children = [
                                v.ListItemTitle(
                                    style_ = "font-size:0.85rem;",
                                    children = [item['title']],
                                ),
                            ],
                        ),
                    ],
                ) for item in sub_items]
            )]
            self.menu_to_work_area += sub_menu[0].children
            return sub_menu

        list_menu = []
        for item in self.app_config.side_nav_menu:
            if item.get("sub_menu"):
                list_menu.append(
                    v.ListGroup(
                        ripple = False,
                        prepend_icon = item["icon"],
                        v_slots = [{
                            "name": "activator",
                            "children": v.ListItemContent(
                                style_ = "padding-left:15px; color:#ffffff;",
                                children = [
                                    v.ListItemTitle(
                                        style_ = "font-size:0.9rem;",
                                        children = [item['title']]
                                    ),
                                ],
                            ),
                        }],
                        children = _make_sub_menu(item['sub_menu']),
                    )
                ) 
            else:
                list_item = v.ListItem(
                                class_ = item['workflow_class_name'],
                                style_ = "",  
                                active = False,
                                ripple = False,
                                children = [
                                    v.ListItemIcon(
                                        style_ = "min-width:30px; max-width:30px; margin:0; padding:0; align-self:center;",
                                        children = [v.Icon(
                                            style_ = "color:#ffffff; font-size:20px;",
                                            children = [item['icon']]
                                            )]
                                    ),
                                    v.ListItemContent(
                                        style_ = "padding-left:15px; color:#ffffff;",
                                        children = [
                                            v.ListItemTitle(
                                                style_ = "font-size:0.9rem;",
                                                children = [item['title']],
                                            ),
                                        ],
                                    ),
                                ],
                            )
                list_menu.append(
                    v.ListItemGroup(
                        style_ = "margin-bottom:8px;",
                        children = [list_item],
                    )
                )

                self.menu_to_work_area.append(list_item)
            
        super().__init__(
            style_ = "",
            nav = True,
            color = "#0f172a",
            children =list_menu,
        )

        self.clicked_item = None
        def _on_click_to_workflow(widget, event, data):
            if self.clicked_item: # if not first click
                self.clicked_item.disabled = None
                
            self.clicked_item = widget # keep last clicked item
            widget.disabled = True # disable clicked item
            
            self.app_context.SideNav.toggle_side_nav()
            self.app_context.WorkArea.children = [
                get_or_create_class(self.app_config.class_path[widget.class_], self.app_context, self.app_config)
                ]


        for item in self.menu_to_work_area:
            item.on_event('click', _on_click_to_workflow)
