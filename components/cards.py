import ipyvuetify as v
from matplotlib.pyplot import title

class BaseCard(v.Card):

    def __init__(
        self, 
        header_title:str = "",  
        header_bottom:object = None, 
        body_items:list = [], 
        body_size:dict = {}, 
        align:str = "", 
        more:bool = True,
        close:bool = False,
        **kwargs
        ):
        
        num_body_items = len(body_items)
        self.body_border_bottom = kwargs.get('body_border_bottom') if kwargs.get('body_border_bottom') else [True for i in range(num_body_items)]
        self.body_background_color = kwargs.get('body_background_color') if kwargs.get('body_background_color') else [None for i in range(num_body_items)]


        self.style = {
            'card': f"width:{body_size.get('width')}; border-radius:8px 8px 8px 8px; border:1px solid #e0e0e0; align-self:{align};",
            'card_header': "padding:0; flex-direction:column; background-color:rgb(248, 250, 252); border-bottom:1px solid #e0e0e0;" + \
                ("height:94px;" if header_bottom else "height:60px;"),
            'card_header_top': "margin:0px; width:100%;",
            'title': "padding:16px 32px 0px 24px; \
                    max-height: 48px; font-size:1rem; \
                    font-weight:bold; color: rgb(30, 41, 59); ",
            'more_menu': "max-width:60px;",
            'close_button': "max-width:60px;",
            'card_body': [
                f"height:{body_size.get('height')[n]}; \
                overflow-y:auto; \
                padding:0px; margin:0px;" \
                + f"{'border-bottom:1px solid #e0e0e0;' if self.body_border_bottom[n] else ''}" \
                + f"{'background-color:' + self.body_background_color[n] + ';' if self.body_background_color[n] else ''}" 
                for n in range(num_body_items)
            ],
            'card_footer': "background-color:rgb(248, 250, 252); padding:0; height:20px;",
        }

    # card header ------------------------------------------------------------
        # card title
        self.title = v.Col(
            children = [header_title],
            style_ = self.style['title'],
        )

        # more menu
        self.more_menu  = ""
        if more:
            self.more_items = v.List(
                children = ["고급 설정"]
            )   
            self.more_button = v.Btn(
                v_on='menu_data.on',
                icon = True,
                children=[v.Icon(children = "mdi-dots-vertical")], 
            )
            self.more_menu = v.Col(
                style_ = self.style['more_menu'],
                children = [
                    v.Menu(
                        offset_y=True,
                        attach=True,
                        v_slots=[{
                            'name': 'activator',
                            'variable': 'menu_data',
                            'children': self.more_button,
                        }],
                        children=[
                            v.List(children=[self.more_items]),
                        ],
                    ),    
                ],
            )

        # close button
        self.close_button_col = ""
        if close:
            self.app_context = kwargs.get('app_context')
            close_button = v.Btn(
                        icon = True,
                        children = [v.Icon(children = "mdi-close")],
                    )
            self.close_button_col = v.Col(
                style_ = self.style['close_button'],
                children = [
                    close_button,
                ],
            )
            
            def _close_window(item, event=None, data=None):
                train_result = self.app_context.tabular_ai_training__train_result
                train_result.close()

            close_button.on_event('click', _close_window)

        # merge title and more, close button
        self.card_header_top = v.Row(
            style_ = self.style['card_header_top'],
            children = [self.title, self.more_menu, self.close_button_col ]
        )

        self.card_header_bottom = header_bottom if header_bottom else ""

        self.card_header = v.CardTitle(
            style_ = self.style['card_header'],
            children = [self.card_header_top, self.card_header_bottom],
        )

        # card footer ------------------------------------------------------------
        self.card_footer = v.CardText(
            style_ = self.style['card_footer'],
        )

        # card body --------------------------------------------------------------
        self.card_body = [v.CardText(
                style_ = self.style['card_body'][n],
                children = [body_item]
            )for n, body_item in enumerate(body_items)]

        self.children = [self.card_header, *self.card_body, self.card_footer]
        
        super().__init__(
            class_ = kwargs.get('class_'),
            style_ = self.style['card'],
            children = self.children,
        )

class SmallHeaderCard(v.Card):
    def __init__(
        self, 
        title:str = "",
        body:object = None,
        size:dict = {},
        **kwargs
        ):
            
        self.style = {
            "card": f"width:{size.get('width')}; height:{size.get('height')}; \
                padding:0; display:flex; flex-direction:column; \
                box-shadow: none !important; \
                background-color: #ffffff00; ",
            "header": "max-height:33px; min-height:33px; margin:0; \
                font-size: 0.875rem; color:rgb(100, 116, 139); \
                align-content:flex-end; padding-left:16px;",
            "body": "padding:0;"
        }

        self.header = v.Row(
            class_ = "",
            style_ = self.style['header'],
            children = [title],
        )
        self.body = v.CardText(
            class_ = "",
            style_ = self.style['body'],
            children = [body]
        )

        super().__init__(
            class_ = "",
            style_ = self.style['card'],
            children = [self.header, self.body],
        )

class SimpleCard(v.Card):
    def __init__(
        self,
        title:str = "",
        body:object = None,
        size:dict = {},
        **kwargs
        ):
            
        self.style = {
            "card": f"width:{size.get('width')}; height:{size.get('height')}; \
                padding:0; display:flex; flex-direction:column; \
                box-shadow: none !important; \
                background-color: #ffffff00; ",
            "header": "max-height:33px; min-height:33px; margin:0; \
                font-size: 0.875rem; color:rgb(100, 116, 139); \
                align-content:flex-end; padding-left:16px;",
            "body": "padding:0;"
        }

        self.header = v.CardTitle(
            class_ = "",
            style_ = self.style['header'],
            children = [title],
        )
        self.body = v.CardText(
            class_ = "",
            style_ = self.style['body'],
            children = [body]
        )

        super().__init__(
            class_ = "",
            style_ = self.style['card'],
            children = [self.header, self.body],
        )