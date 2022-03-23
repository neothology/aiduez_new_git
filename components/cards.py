import ipyvuetify as v
from matplotlib.pyplot import title
from components.dialog import SimpleDialog

class BaseCard(v.Card):

    def __init__(
        self, 
        header_title_main:str = "", 
        header_title_sub:str = "", 
        header_bottom:object = None, 
        body_items:list = [], 
        body_size:dict = {}, 
        align:str = "", 
        more:bool = True,
        close:bool = False,
        save:bool = False,
        **kwargs
        ):
        
        self.app_context = kwargs.get('app_context')

        num_body_items = len(body_items)
        self.body_border_bottom = kwargs.get('body_border_bottom') if kwargs.get('body_border_bottom') else [True for i in range(num_body_items)]
        self.body_background_color = kwargs.get('body_background_color') if kwargs.get('body_background_color') else [None for i in range(num_body_items)]


        self.style = {
            'card': f"width:{body_size.get('width')}; border-radius:8px 8px 8px 8px; border:1px solid #e0e0e0; align-self:{align};",
            'card_header': "padding:0; flex-direction:column; background-color:rgb(248, 250, 252); border-bottom:1px solid #e0e0e0;" + \
                ("height:94px;" if header_bottom else "height:60px;"),
            'card_header_top': "margin:0px; width:100%;" + f"{'max-height:59px;' if header_bottom else ''}",
            'title_main': "padding:16px 32px 0px 24px; \
                    max-height: 48px; font-size:1rem; \
                    font-weight:bold; color: rgb(30, 41, 59); ",
            'title_sub': "padding:16px 32px 0px 24px; \
                    max-height: 48px; font-size:1rem; \
                    font-weight:bold; color: rgb(30, 41, 59); ",
            'more_menu': f'{"max-width:40px;" if close else "max-width:60px;"}',
            'save_button': "max-width:40px;",
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

        if kwargs.get('style'):
            for key, val in kwargs.get('style').items():
                self.style[key] = val


    # card header ------------------------------------------------------------
        # card title_main
        self.title_main = v.Col(
            children = [header_title_main],
            style_ = self.style['title_main'],
        )

        # card title_sub
        self.title_sub = ""
        if header_title_sub != "":
            self.title_sub = v.Col(
                children = [header_title_sub],
                style_ = self.style['title_sub'],
            )

        # more menu
        self.more_menu_col = ""
        if more:
            self.more_items = v.List(
                children = ["고급 설정"]
            )   
            self.more_button = v.Btn(
                v_on='menu_data.on',
                disabled = True,
                icon = True,
                children=[v.Icon(children = "mdi-dots-vertical")], 
            )
            self.more_menu_col = v.Col(
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
            self.close_button = v.Btn(
                icon = True,
                disabled = True,
                children = [v.Icon(children = "mdi-close")],
            )

            self.close_button_col = v.Col(
                style_ = self.style['close_button'],
                children = [
                    self.close_button,
                ],
            )
            
            def _close_window(item, event=None, data=None):
                train_result = self.app_context.tabular_ai_training__train_result
                train_result.close()
                self.more_button.disabled = True
                self.save_button.disabled = True
                self.close_button.disabled = True

            self.close_button.on_event('click', _close_window)

        # save button
        self.save_button_col = ""
        if save:
             # model save as (dialog)
            self.model_save_body = v.TextField(
                v_model = "",
                prefix = "",
            )

            self.save_confrim_btn = v.Btn(
                children = ["저장"],
            )

            def save_model_as(item, event=None, data=None):
                self.app_context.tabular_model.save_as(self.model_save_body.prefix, self.model_save_body.v_model)
                self.model_save_dialog.value = 0

            self.save_confrim_btn.on_event('click', save_model_as)

            self.save_cancel_btn = v.Btn(
                children = ["취소"],
            )

            def cancel_save_model_as(item, event=None, data=None):
                self.model_save_dialog.value = 0

            self.save_cancel_btn.on_event('click', cancel_save_model_as)

            self.model_save_dialog = SimpleDialog(
                title = "다른 이름으로 저장",
                body = self.model_save_body,
                buttons = [ self.save_confrim_btn, self.save_cancel_btn ],
                size = {'width':'500px', 'height':'200px'},
            )
            self.save_button = v.Btn(
                v_on = 'tooltip.on',
                disabled = True,
                icon = True,
                children = [
                    v.Icon(
                        class_ = 'material-icons',
                        children = "save_alt",
                    ),
                ],
            )

            def _on_click_save_button(item, event=None, data=None):
                self.model_save_dialog.show()

            self.save_button.on_event('click', _on_click_save_button)

            save_tooltip_button = v.Tooltip(
                bottom = True,
                v_slots = [{
                    'name': 'activator',
                    'variable': 'tooltip',
                    'children': [self.save_button],
                }],
                children = ['다른 이름으로 저장'],
            )

            self.save_button_col = v.Col(
                style_ = self.style['save_button'],
                children = [self.model_save_dialog, save_tooltip_button],
            )       

        # merge titles and more, close button
        self.card_header_top = v.Row(
            style_ = self.style['card_header_top'],
            children = [
                self.title_main, 
                self.title_sub,
                self.save_button_col, 
                self.more_menu_col, 
                self.close_button_col ]
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

    def update_body_items(self, body_items):
        self.card_body = [v.CardText(
                style_ = self.style['card_body'][n],
                children = [body_item]
            )for n, body_item in enumerate(body_items)]
        self.children = [self.card_header, *self.card_body, self.card_footer]



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
        buttons:list = None,
        size:dict = {},
        **kwargs
        ):
        self.buttons = buttons
        self.style = {
            "card": f"width:{size.get('width')}; height:{size.get('height')}; \
                padding:0; display:flex; flex-direction:column; \
                box-shadow: none !important; \
                background-color: rgb(255, 255, 255); ",
            "header": "max-height:33px; min-height:33px; margin:0; \
                font-size: 0.875rem; color:rgb(100, 116, 139); \
                padding:0; padding-left:16px; \
                background-color:rgb(248, 250, 252); \
                border-bottom:1px solid #e0e0e0;",
            "body": "padding:0px; margin:0px; background-color:rgb(255, 255, 255); \
                padding-left: 20px; padding-right: 20px; \
                display:flex; align-items:center; height:150px;",
            "footer": "background-color:rgb(255, 255, 255); \
                justify-content:flex-end; padding-right:20px;" 
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

        self.footer = v.CardActions(
            class_ = "",
            style_ = self.style['footer'],
            children = [
                self.buttons[0],
                self.buttons[1],
            ],
        )


        super().__init__(
            class_ = "",
            style_ = self.style['card'],
            children = [self.header, self.body, self.footer],
        )