import ipyvuetify as v
from utils import get_or_create_class, set_theme_style

class ListMenu(v.List):

    def __init__(self, app_context, context_key, **kwargs):
        self.app_context = app_context
        self.context_key = context_key
        self.menu_to_target = [] # to collect menus to be clicked

        def _make_sub_menu(sub_items: list) -> list:

            sub_menu = [v.ListItemGroup(
                class_ = "main-menu-group",
                style_ = "",
                children = [v.ListItem(
                    class_ = "",
                    value = item["target"],
                    style_ = "padding-left:32px;",
                    active = False,
                    ripple = False,
                    children = [
                        v.ListItemIcon(
                            style_ = set_theme_style(self.app_context, self.context_key, elem='list_item_icon'),
                            children = [v.Icon(
                                style_ = set_theme_style(self.app_context, self.context_key, elem='list_item_icon_icon'),
                                children = [item['icon']])]
                        ),
                        v.ListItemContent(
                            style_ = set_theme_style(self.app_context, self.context_key, elem='list_item_contents'),
                            children = [
                                v.ListItemTitle(
                                    style_ = set_theme_style(self.app_context, self.context_key, elem='list_item_title'),
                                    children = [item['title']],
                                ),
                            ],
                        ),
                    ],
                ) for item in sub_items]
            )]
            self.menu_to_target += sub_menu[0].children
            return sub_menu

        list_menu = []
        for item in self.app_context.side_nav_menu_list['menu_list']:
            if item.get("sub_menu"):
                list_menu.append(
                    v.ListGroup(
                        class_ = "main-menu-group",
                        ripple = False,
                        prepend_icon = item["icon"],
                        v_slots = [{
                            "name": "activator",
                            "children": v.ListItemContent(
                                style_ = set_theme_style(self.app_context, self.context_key, elem='list_item_contents'),
                                children = [
                                    v.ListItemTitle(
                                        style_ = set_theme_style(self.app_context, self.context_key, elem='list_item_title'),
                                        children = [item['title']]
                                    ),
                                ],
                            ),
                        }],
                        children = _make_sub_menu(item['sub_menu']),
                        style_ = 'margin-bottom:8px; margin-left:-2px;',
                    )
                ) 
            else:
                list_item = v.ListItem(
                                value = item['target'],
                                style_ = "",  
                                active = False,
                                ripple = False,
                                children = [
                                    v.ListItemIcon(
                                        style_ = set_theme_style(self.app_context, self.context_key, elem='list_item_icon'),
                                        children = [v.Icon(
                                            style_ = set_theme_style(self.app_context, self.context_key, elem='list_item_icon_icon'),
                                            children = [item['icon']]
                                            )]
                                    ),
                                    v.ListItemContent(
                                        style_ = "padding-left:15px; color:#ffffff;",
                                        children = [
                                            v.ListItemTitle(
                                                style_ = set_theme_style(self.app_context, self.context_key, elem='list_item_title'),
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

                self.menu_to_target.append(list_item)

        super().__init__(
            class_ = self.context_key,
            style_ = set_theme_style(self.app_context, self.context_key),
            nav = True,
            color = "#0f172a",
            children =list_menu,
        )       

        self.last_activated_item = None
        def _proceed_to_target(item, event=None, data=None): 

            task_type = item.value.split('_')[0] # code_add: to use different workbook by task_type

            # set 'active' to last activated item wihich is now deactivated
            if self.last_activated_item:
                self.last_activated_item.disabled = False  

            # disable clicked item and keep it as last activated item
            if task_type == 'task':
                item.disabled = True

            self.last_activated_item = item

            # get target and set
            self.app_context.current_workflow = task_type  
            if task_type != 'task':
                target_instance = get_or_create_class(item.value, self.app_context) # item.value = tabluar, text, image, video, audio, etc ~base
                target_instance.create_new()

            else:        
                target_instance = get_or_create_class(item.value, self.app_context) # item.value = 'task_recent, task_favorite, task_all'
                target_instance.load_workbook_profiles_and_show()

            # other actions
            if task_type == 'task':
                
                # (1) change nav_bar props
                self.app_context.side_nav.temporary = False
                self.app_context.side_nav.permanent = True
                self.app_context.side_nav.v_model = True

                # (2) change top area props according to target
                self.app_context.top_area.change_style('light')
                self.app_context.work_area.change_style('light')

            else:

                self.app_context.side_nav.temporary = True
                self.app_context.side_nav.permanent = False
                self.app_context.side_nav.v_model = False
                self.app_context.top_area.change_style('default')
                self.app_context.work_area.change_style('default')

        # set default
        default_target_name: str = self.app_context.side_nav_menu_list['default'] # task_recent_view
        default_menu_item = list(filter(lambda x: x.value == default_target_name, self.menu_to_target))[0] # value = task_recent_view
        _proceed_to_target(default_menu_item)

        # set event listener
        for item in self.menu_to_target:
            item.on_event('click', _proceed_to_target)
