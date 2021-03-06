from importlib.abc import FileLoader
from click import style
import ipyvuetify as v
import ipywidgets
from components.cards import SimpleCard


class DataSelect(v.Select):
    def __init__(self, index:int, items, v_model, **kwargs):
        self.index = index

        super().__init__(
            items = items,
            v_model = v_model,
            attach = True,
            label = kwargs.get('label'),
            dense = kwargs.get('dense'),
            outlined = kwargs.get('outlined'),
            solo = kwargs.get('solo'),
            filled = kwargs.get('filled'),
            hide_details = kwargs.get('hide_details'),
            readonly = kwargs.get('readonly'),
            class_ = kwargs.get('class_'),
            style_ = kwargs.get('style_'),
        )


class LabeledSelect(v.Col):
    def __init__(self, index:int, label:str, items, v_model, **kwargs):
        self.index = index

        label = v.Subheader(
            style_ = "height: 10px; padding-top:15px; padding-right:0; width:87px",
            children = [label],
        )
        
        selector = v.Select(
            items = items,
            v_model = v_model,
            attach = True,
            dense = kwargs.get('dense'),
            outlined = kwargs.get('outlined'),
            solo = kwargs.get('solo'),
            filled = kwargs.get('filled'),
            hide_details = kwargs.get('hide_details'),
            class_ = kwargs.get('class_'),
            readonly = kwargs.get('readonly'),
            style_ = "width:133px; padding-right:10px; padding-top:10px",
        )

        super().__init__(
            class_ = kwargs.get('class_'),
            style_ = kwargs.get('style_'),
            children = [
                v.Row(
                    children = [label, selector],
                    style_ = "margin:0; max-height:30px;",
                    ),
            ],
        )


class DataSlider(v.Col):
    def __init__(self, index:int = None, label:str = "", range:list = [], **kwargs):
        self.index = index
   
        label = v.Subheader(
            style_ = "height: 10px; padding-top:15px; width:150px;",
            children = [label],
        )

        slider = v.Slider(
            min = range[0],
            max = range[1],
            step = range[2],
            v_model = range[3],
            dense = kwargs.get('dense'),
            hide_details = True,
            style_ = "padding:0; min-width:150px; height:25px; \
                margin-left:8px; margin-right:2px;",
        )

        counter = v.TextField(
            v_model = range[3],
            dense = kwargs.get('dense'),
            style_ = "max-width:60px;",
        )

        ipywidgets.jslink((slider, 'v_model'), (counter, 'v_model'))

        super().__init__(
            class_ = kwargs.get('class_'),
            style_ = kwargs.get('style_'),
            children = [
                v.Row(
                    children = [label, counter],
                    style_ = "margin:0; max-height:30px;",
                    ),
                slider,
            ],
        )

class SimpleSlider(v.Row):
    def __init__(self, range:list = [], **kwargs):

        slider = v.Slider(
            min = range[0],
            max = range[1],
            step = range[2],
            v_model = range[3],
            dense = True,
            hide_details = True,
            style_ = "padding:0; height:25px; \
                margin: 15px 2px 0 8px;",
        )

        counter = v.TextField(
            v_model = range[3],
            filled = True,
            dense = True,
            hide_details = True,
            style_ = "max-width:90px; padding:3px",
        )

        ipywidgets.jslink((slider, 'v_model'), (counter, 'v_model'))

        super().__init__(
            class_ = kwargs.get('class_'),
            style_ = "margin:0;", # border:1px solid #e0e0e0; border-radius:20px; background-color:#fff;",
            children = [
                slider,
                counter
            ],
        )
class SimpleInputCard(SimpleCard):
    def __init__(
        self,
        app_context:object = None, 
        context_key:str = "",  
        title:str = "",
        size:dict = {},
        **kwargs
    ):

        input = v.TextField(
            style_ = "max-width:200px; margin:0;",
            single_line = True,
            v_model= None
        )

        body = v.Row(
            children = [
                input,
            ],
            style_ = "margin:0; padding-left:22px; padding-bottom:10px; align-items:center;" + kwargs.get('style', ""),        )

        super().__init__(
            class_ = kwargs.get('class_'),
            title= title,
            body = body,
            no_footer=True,
            size = size,
        )

class SimpleSliderCard(SimpleCard):
    def __init__(
        self,
        app_context:object = None, 
        context_key:str = "",  
        title:str = "",
        range:list = [], 
        size:dict = {},
        **kwargs
    ):

        slider = v.Slider(
            min = range[0],
            max = range[1],
            step = range[2],
            v_model = range[3],
            dense = True,
            hide_details = True,
            style_ = "padding:0; height:25px;"
        )

        counter = v.TextField(
            class_ = "extra-dense",
            v_model = range[3],
            dense = True,
            hide_details = True,
            style_ = "max-width:100px; margin:0;",
        )

        ipywidgets.jslink((slider, 'v_model'), (counter, 'v_model'))

        body = v.Row(
            children = [
                slider,
            ],
            style_ = "margin:0; padding-bottom:10px; align-items:center;" + kwargs.get('style', ""), 
        )

        super().__init__(
            class_ = kwargs.get('class_'),
            title= title,
            body = body,
            controls = [counter],
            no_footer=True,
            size = size,
        )

class SimpleRadioCard(SimpleCard):
        def __init__(
            self,
            app_context:object = None, 
            context_key:str = "",  
            title:str = "",
            direction:str = "",
            options:dict = {}, 
            size:dict = {},
            **kwargs
        ):
            self.direction = True if direction == 'row' else False

            radio_options = v.RadioGroup(
                class_ = context_key,
                v_model = options['values'][0],
                row = self.direction,
                style_ = "padding:0; height:25px;",
                children = [
                    v.Radio(
                        label = option[0],
                        value = option[1],
                    ) for option in zip(options['labels'], options['values'])],
            )

            self.selected_option = radio_options.v_model
            def on_change_radio(item, event, data):
                self.selected_option = item.v_model
            radio_options.on_event('change', on_change_radio)

            body = v.Row(
                children = [radio_options],
                style_ = "margin:0; padding-bottom:10px; align-items:center; padding-left:15px;" + kwargs.get('style', ""), 
            )

            super().__init__(
                class_ = kwargs.get('class_'),
                title= title,
                body = body,
                no_footer=True,
                size = size,
            )

class SimpleRangeCard(SimpleCard):
    def __init__(
        self,
        app_context:object = None, 
        context_key:str = "",  
        title:str = "",
        direction:str = "",
        options:dict = {}, 
        size:dict = {},
        range:list = [], 
        **kwargs
    ):
        self.direction = True if direction == 'row' else False

        slider = v.Slider(
            min = range[0],
            max = range[1],
            step = range[2],
            v_model = range[3],
            dense = True,
            hide_details = True,
            style_ = "margin-left: 24px; max-width:250px; padding:0; height:25px;"
        )

        counter = v.TextField(
            class_ = "extra-dense",
            v_model = range[3],
            dense = True,
            hide_details = True,
            style_ = "max-width:100px; margin:0;",
        )

        ipywidgets.jslink((slider, 'v_model'), (counter, 'v_model'))

        body = v.Row(
            children = [
                slider,
            ],
            style_ = "margin:0; padding-bottom:10px; align-items:center;" + kwargs.get('style', ""), 
        )

        super().__init__(
            class_ = kwargs.get('class_'),
            title= title,
            body = body,
            controls = [counter],
            no_footer=True,
            size = size,
        )

class SelectAutoComplete(v.Autocomplete):
    def __init__(
        self,
        label:str="",
        items:list=[],
        size:dict={'width':'210px', 'height':'200px'},
        style:str="",
        **kwargs
        ):
        self.value = ""     # autocomplete??? ?????? ???
        self.label = label
        self.items = items  # autocomplete??? item list

        style += f"width:{size['width']}; height:{size['height']};"

        super().__init__(
            v_model=self.value,
            items=self.items,
            label=self.label,
            style_=style,
            attach=True
        )

    def change_value(self, widget, event=None, data=None):
        self.value = widget.v_model

class SimpleDataTableCard(SimpleCard):
    def __init__(
        self,
        app_context:object = None, 
        context_key:str = "",  
        title:str = "",
        direction:str = "",
        options:dict = {}, 
        size:dict = {},
        range:list = [],
        datatable:object = None, 
        **kwargs
    ):
        self.direction = True if direction == 'row' else False
        
        self.datatable=datatable

        body = v.Col(
            children = [
                self.datatable
            ],
            style_ = "margin:0; padding-bottom:10px; align-items:center; vertical-align: top; !important;" + kwargs.get('style', ""), 
        )

        super().__init__(
            class_ = kwargs.get('class_'),
            title= title,
            body = body,
            no_footer=True,
            size = size,
        )
