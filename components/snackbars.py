import ipyvuetify as v

class ChartFrame(v.Col):
    def __init__(
        self, 
        title:str = "", 
        src:str = "", 
        size:dict = {}, 
        **kwargs
        ):

        self.style = {
            "frame": f"width:{size.get('width')}; height:{size.get('height')}; padding:0; display:flex; flex-direction:column; ",
            "header": "max-height:34px; min-height:34px; margin:0; \
                border-bottom:1px solid #e0e0e0; background-color:#f1f1f1; \
                font-size: 0.875rem; color:rgb(100, 116, 139); \
                align-content:center; justify-content:center;",
            "body": "border:0; height:calc(100% - 33px);",
        }

        self.header = v.Row(
            class_ = "chartframe-header",
            style_ = self.style['header'],
            children = [title],
        )
        self.body = v.Html(
            tag = 'iframe',
            attributes = {
                'class': 'chartframe-body',
                'src': src,
                'style': self.style['body'],
                },
        )

        # self.body = IFrame(src, width=size.get('width'), height=size.get('height'))

        super().__init__(
            style_ = self.style['frame'],
            children = [self.header, self.body],
        )
