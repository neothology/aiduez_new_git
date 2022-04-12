import ipyvuetify as v
from utils import get_or_create_class

class TabMenu(v.Col):

    def __init__(self, app_context, context_key, target_area, tab_props, tab_name, update=False, **kwargs):
        self.app_context = app_context
        self.context_key = context_key
        self.target_area = target_area
        self.tab_props = tab_props
        self.tab_name = tab_name

        self.update = update

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
                    value = stage['target'],
                    children = stage['title'],
                    ) for stage in self.tab_props['stages']
            ],
        )

        # make tab_menu_border_bottom_bloc item(inactive)
        self.tab_menu_border_bottom_block = v.Row(
            style_ = "height:3px; margin:-2px 0; position:relative;",
            children = [v.Col(style_=inactive_style["block"]) for _ in range(len(self.tab_props['stages']))],
        )

        # gather stage['target'] for later use
        self.tab_stage_targets = [stage['target'] for stage in self.tab_props['stages']]

        super().__init__(
            class_ = self.context_key,
            style_ = "margin-top:-36px !important; padding:0 70px; backgroung-color: none; max-height:37px; z-index:777;",
            children = [self.tab_menu, self.tab_menu_border_bottom_block]
        )
        
        self.last_activated_tab = None 
        def _proceed_to_target(tab, event=None, data=None):

            # validation: check if current data is set (except:'data import')
            if tab.value != "tabular_data_import" and self.app_context.current_workflow == 'tabular':
                if self.app_context.tabular_dataset.current_data is None:
                    return

            # enable last activated tab, if any
            if self.last_activated_tab:
                self.last_activated_tab.disabled = False 
                self.last_activated_tab.style_ = inactive_style["tab"]
                tab_value = self.tab_stage_targets.index(self.last_activated_tab.value)
                self.tab_menu_border_bottom_block.children[tab_value].style_ = inactive_style["block"]
                
            # disable clicked tab
            tab.disabled = True
            tab.style_ = active_style["tab"]
            tab_value = self.tab_stage_targets.index(tab.value)
            self.tab_menu_border_bottom_block.children[tab_value].style_ = active_style["block"]

            # keep last activated item
            self.last_activated_tab = tab 

            # get target and set
            self.app_context.current_workflow_stage = tab.value
            target_instance = get_or_create_class(tab.value, self.app_context, update = self.update)
        
            self.target_area.children = [target_instance]

            # temporary code for 'training': 
            if tab.value == 'tabular_ai_training':
                target_instance.load_contents()

        for tab in self.tab_menu.children:
            tab.on_event('click', _proceed_to_target)

        # set tab
        tab = list(filter(lambda x: x.value == self.tab_name, self.tab_menu.children))[0]

        _proceed_to_target(tab)

class ListMenuSub(v.List):

    def __init__(
        self, 
        app_context, 
        context_key, 
        menu_tree,
        **kwargs):

        self.app_context = app_context
        self.context_key = context_key
        self.menu_tree = menu_tree
        self.menu_to_target = [] # to collect menus to be clicked

        

        self.style = {
            'background': 'background-color: #ffffff00;',
            'list_title': 'color: #5a5a5a; font-size: 14px;',
            'icon': 'color: #5a5a5a; font-size: 20px; margin-right:0px;',


        }

        def _make_sub_menu(sub_items: list) -> list:

            sub_menu = [v.ListItemGroup(
                class_ = "",
                style_ = "",
                children = [v.ListItem(
                    class_ = "sub-menu-item",
                    value = item["target"],
                    style_ = "padding-left:32px;",
                    active = False,
                    ripple = False,
                    children = [
                        v.ListItemIcon(
                            style_ = self.style['icon'],
                            children = [v.Icon(
                                style_ = self.style['icon'],
                                children = [item['icon']])]
                        ),
                        v.ListItemContent(
                            style_ = "padding-left:12px;",
                            children = [
                                v.ListItemTitle(
                                        style_ = self.style['list_title'],
                                        children = [item['title']]
                                    ),
                                v.ListItemSubtitle(
                                    style_ = "font-size:10px;",
                                    children = [item['sub_title']]
                                ),
                            ],
                        ),
                    ],
                ) for item in sub_items]
            )]
            self.menu_to_target += sub_menu[0].children
            return sub_menu

        list_menu = []
        for item in self.menu_tree:
            if item.get("sub_menu"):
                list_menu.append(
                    v.ListGroup(
                        class_ = "sub-menu-group",
                        ripple = False,
                        prepend_icon = item["icon"],
                        v_slots = [{
                            "name": "activator",
                            "children": v.ListItemContent(
                                style_ = "",
                                children = [
                                    v.ListItemTitle(
                                        style_ = self.style['list_title'],
                                        children = [item['title']]
                                    ),
                                ],
                            ),
                        }],
                        children = _make_sub_menu(item['sub_menu']),
                        style_ = 'margin-bottom:8px;',
                    )
                ) 
            else:
                list_item = v.ListItem(
                                class_ = 'sub-menu-item',
                                value = item['target'],
                                style_ = "",  
                                active = False,
                                ripple = False,
                                children = [
                                    v.ListItemIcon(
                                        style_ = self.style['icon'],
                                        children = [v.Icon(
                                            style_ = self.style['icon'],
                                            children = [item['icon']]
                                            )]
                                    ),
                                    v.ListItemContent(
                                        style_ = "padding-left:7px; color:#ffffff;",
                                        children = [
                                            v.ListItemTitle(
                                                style_ = self.style['list_title'],
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
            style_ = self.style['background'],
            nav = True,
            children =list_menu,
        )     

        self.last_activated_item = None
        def _proceed_to_target(item, event=None, data=None):               

            stage = self.context_key.split("__")[0] # e.g. tabular_data_analytics

            if self.last_activated_item:
                self.last_activated_item.class_list.remove("now_active")
            item.class_list.add("now_active")
            self.last_activated_item = item

            # get target and set
            self.app_context.current_workflow_stage_sub = item.value

            # temporary condition to apply MVC:
            if self.app_context.current_workflow_stage != 'tabular_data_analytics':
                target_area = getattr(self.app_context, stage + "__sub_contents")        
                target_instance = get_or_create_class(item.value, self.app_context) # e.g. tabular_analytics_basicinfo의 경우 여기서 options가 생성
                target_area.children = [target_instance]
            else:
                target_instance = get_or_create_class(item.value, self.app_context) 
                target_instance.show_contents()

            if self.last_activated_item != item:
                self.app_context.tabular_data_analytics_options.v_model = True
            else:
                if self.app_context.tabular_data_analytics_options:
                    self.app_context.tabular_data_analytics_options.nav_toggle()
        
        # set event listener
        for item in self.menu_to_target:
            item.on_event('click', _proceed_to_target)