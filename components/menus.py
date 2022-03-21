import ipyvuetify as v
from utils import get_or_create_class, set_theme_style

class ListMenu(v.List):

    def __init__(self, app_context, context_key, **kwargs):
        self.app_context = app_context
        self.context_key = context_key
        self.menu_to_target = [] # to collect menus to be clicked

        def _make_sub_menu(sub_items: list) -> list:

            sub_menu = [v.ListItemGroup(
                class_ = "",
                style_ = "",
                children = [v.ListItem(
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
                        ripple = False,
                        prepend_icon = item["icon"],
                        v_slots = [{
                            "name": "activator",
                            "children": v.ListItemContent(
                                style_ = set_theme_style(self.app_context, self.context_key, elem='list_item_contents'),
                                children = [
                                    v.ListItemTitle(
                                        style_ = set_theme_style(self.app_context, self.context_key, elem='list_item_title', style_type='small'),
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

        # # add save button
        # btn_save = v.Btn(
        #     children = "저장하기",
        # )

        # list_menu.append(
        #     v.Row(
        #         children = [btn_save],
        #     )
        # )

        super().__init__(
            class_ = self.context_key,
            style_ = set_theme_style(self.app_context, self.context_key),
            nav = True,
            color = "#0f172a",
            children =list_menu,
        )     

        self.last_activated_item = None
         # code_add: run progress circular: with...
        def _proceed_to_target(item, event=None, data=None): 

            task_type = item.value.split('_')[0] # code_add: to use different workbook by task_type

            # set 'active' to last activated item wihich is now deactivated
            if self.last_activated_item:
                self.last_activated_item.disabled = False  

            # disable clicked item and keep it as last activated item
            item.disabled = True
            self.last_activated_item = item

            # get target and set
            self.app_context.current_workflow = task_type  
            target_area = get_or_create_class(self.app_context.side_nav_menu_list['target_area'], self.app_context) # work_area           
            target_instance = get_or_create_class(item.value, self.app_context) # tabluar, text, image, video, audio, etc ~base
            target_area.children = [target_instance]

            # other actions
            if task_type == 'task':
                
                # (1) change nav_bar props
                self.app_context.side_nav.temporary = False
                self.app_context.side_nav.permanent = True
                self.app_context.side_nav.v_model = True

                # (2) change top area props according to target
                self.app_context.top_area.change_style('light')
            else:

                self.app_context.side_nav.temporary = True
                self.app_context.side_nav.permanent = False
                self.app_context.side_nav.v_model = False
                self.app_context.top_area.change_style('default')

        # set default
        default_target_name: str = self.app_context.side_nav_menu_list['default']
        default_menu_item = list(filter(lambda x: x.value == default_target_name, self.menu_to_target))[0]
        _proceed_to_target(default_menu_item)

        # set event listener
        for item in self.menu_to_target:
            item.on_event('click', _proceed_to_target)

        

class TabMenu(v.Col):

    def __init__(self, app_context, context_key, target_area, **kwargs):
        self.app_context = app_context
        self.context_key = context_key
        self.target_area = target_area
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
                tab_value = self.tab_stage_targets.index(self.last_activated_tab.value)
                self.tab_menu_border_bottom_block.children[tab_value].style_ = inactive_style["block"]
                
            # disable clicked tab
            tab.disabled = True
            tab.style_ = active_style["tab"]
            tab_value = self.tab_stage_targets.index(tab.value)
            self.tab_menu_border_bottom_block.children[tab_value].style_ = active_style["block"]

            # keep last activated item
            self.last_activated_tab = tab 

            # add - run progress circular: with...

            # get target and set
            self.app_context.current_workflow_stage = tab.value
            target_instance = get_or_create_class(tab.value, self.app_context) # for example, tab.value = "tabular_ai_training"
            self.target_area.children = [target_instance]

        # set default
        default_tab_name: str = self.tab_props['default']
        default_tab = list(filter(lambda x: x.value == default_tab_name, self.tab_menu.children))[0]
        _proceed_to_target(default_tab)
        
        for tab in self.tab_menu.children:
            tab.on_event('click', _proceed_to_target)

