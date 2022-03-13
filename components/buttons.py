import ipyvuetify as v

class StatedBtn(v.Btn):
    def __init__(self, index:int, state:str, children:list, **kwargs):
        self.index = index
        self.state = state

        super().__init__(
            v_on = kwargs.get('v_on'),
            icon = kwargs.get('icon'),
            style_ = kwargs.get('style_'),
            color = kwargs.get('color'),
            children = children,
        )
