import ipyvuetify as v
from utils import get_or_create_class

class ListMenu(v.List):

    def __init__(self, app_context, app_config, **kwargs):
        self.app_context = app_context
        self.app_config = app_config
        self.menu_to_target = [] # to collect menus to be clicked

        def _make_sub_menu(sub_items: list) -> list:

            sub_menu = [v.ListItemGroup(
                class_ = "",
                style_ = "",
                children = [v.ListItem(
                    class_ = item["target"],
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
            self.menu_to_target += sub_menu[0].children
            return sub_menu

        list_menu = []
        for item in self.app_config.side_nav_menu['menu_list']:
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
                                class_ = item['target'],
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

                self.menu_to_target.append(list_item)
            
        super().__init__(
            style_ = "",
            nav = True,
            color = "#0f172a",
            children =list_menu,
        )     

        self.last_activated_item = None
        def _proceed_to_target(item, event=None, data=None): 
            if self.last_activated_item:
                self.last_activated_item.disabled = False  

            item.disabled = True # disable activated item
            self.last_activated_item = item # keep last activated item

            # get target and set
            target_area = get_or_create_class(self.app_config.side_nav_menu['target_area'], self.app_context, self.app_config)
            target_instance = get_or_create_class(item.class_, self.app_context, self.app_config)
            target_area.children = [target_instance]

            # other actions
            self.app_context.side_nav.temporary = target_instance.navigation_drawer_props['temporary']
            self.app_context.side_nav.permanent = target_instance.navigation_drawer_props['permanent']
            self.app_context.side_nav.v_model = target_instance.navigation_drawer_props['v_model']
            self.app_context.current_workflow = item.class_

        # set default
        default_target_name: str = self.app_config.side_nav_menu['default']
        default_menu_item = list(filter(lambda x: x.class_ == default_target_name, self.menu_to_target))[0]
        _proceed_to_target(default_menu_item)

        # set event listener
        for item in self.menu_to_target:
            item.on_event('click', _proceed_to_target)

class TabtMenu(v.Col):

    def __init__(self, app_context, app_config, **kwargs):
        self.app_context = app_context
        self.app_config = app_config
        self.tab_props = kwargs.get("tab_props")

        # define active/inactive css style
        active_style = {
            "tab":"height:36px; width:200px; \
                    margin:0 1px; \
                    background-color:#f1f5f9 !important; \
                    border:1px solid #e2e8f0 !important; \
                    border-radius:20px 20px 0 0 / 80px 80px 0 0; \
                    color: #5a5a5a !important; \
                    font-weight:600; \
                    opacity:1;",
            "block":"max-width:198px; margin:0 2px !important; padding:0; background-color:#f1f5f9;",
        }
        inactive_style = {
            "tab":"height:36px; width:200px; \
                    margin:0 1px; \
                    background-color:#5e5e5e; \
                    border:1px solid #e2e8f0 !important; \
                    border-radius:20px 20px 0 0 / 80px 80px 0 0; \
                    color: #bfbfbf; \
                    font-weight:600; \
                    opacity:1;",
            "block":"max-width:198px; margin:0 2px !important; padding:0; background-color:#f1f5f9; opacity:0;",
        }
        
        self.tab_menu = v.BtnToggle(
            class_ = "tab_menu",
            style_ = "background-color:fff0",
            children = [
                v.Btn(
                    style_ = inactive_style["tab"],
                    class_ = stage['key'],
                    children = stage['title'],
                    ) for stage in self.tab_props['stages']
            ],
        )

        # make tab_menu_border_bottom_bloc item(inactive)
        self.tab_menu_border_bottom_block = v.Row(
            style_ = "height:3px; margin:-2px 0; position:relative;",
            children = [v.Col(style_=inactive_style["block"]) for _ in range(len(self.tab_props['stages']))],
        )

        # gather stagey['key'] for later use
        self.tab_stage_keys = [stage['key'] for stage in self.tab_props['stages']]

        super().__init__(
            class_ = kwargs.get("context_key"),
            style_ = "margin-top:-48px !important; padding:0 70px; backgroung-color: none;",
            children = [self.tab_menu, self.tab_menu_border_bottom_block]
        )
        
        self.last_activated_tab = None 
        def _proceed_to_target(tab, event=None, data=None):

            # enable last activated tab, if any
            if self.last_activated_tab:
                self.last_activated_tab.disabled = False 
                self.last_activated_tab.style_ = inactive_style["tab"]
                tab_no = self.tab_stage_keys.index(self.last_activated_tab.class_)
                self.tab_menu_border_bottom_block.children[tab_no].style_ = inactive_style["block"]
                
            # disable clicked tab
            tab.disabled = True
            tab.style_ = active_style["tab"]
            tab_no = self.tab_stage_keys.index(tab.class_)
            self.tab_menu_border_bottom_block.children[tab_no].style_ = active_style["block"]

            # keep last activated item
            self.last_activated_tab = tab 

            # get target and set
            target_area = get_or_create_class('sub_area', self.app_context, self.app_config, context_key = self.tab_props['target_area'])
            target_instance = get_or_create_class(tab.class_, self.app_context, self.app_config)
            target_area.children = [target_instance]
            self.app_context.current_workflow_stage = tab.class_
        
        # set default
        default_tab_name: str = self.tab_props['default']
        default_tab = list(filter(lambda x: x.class_ == default_tab_name, self.tab_menu.children))[0]
        _proceed_to_target(default_tab)

        for tab in self.tab_menu.children:
            tab.on_event('click', _proceed_to_target)

