from utils import get_or_create_class
import ipyvuetify as v
import traitlets
import pandas as pd
from components.forms import DataSelect

color_options=["Greys", "OrRd", "PuBu", "BuPu", "Oranges", "BuGn", "YlOrBr", "YlGn", "Reds", "RdPu", "Greens", "YlGnBu", "Purples", "GnBu", "Greys", "YlOrRd", "PuRd", "Blues", "PuBuGn", "viridis", "plasma", "inferno", "magma",]

class SelectorCard(v.VuetifyTemplate):
    items = traitlets.List([]).tag(sync=True, allow_null=True)  
    selected = traitlets.Unicode(default_value=None, allow_none=True).tag(sync=True)
    style = traitlets.Unicode(default_value=None, allow_none=True).tag(sync=True)
    headline = traitlets.Unicode(default_value=None, allow_none=True).tag(sync=True)

    @traitlets.default('template')
    def _template(self):
        return '''
        <template>
            <div>
                <v-card class="mx-auto" width="208px" style="box-shadow: unset; ">
                    <v-card style="align-content: space-around; outline-style: none; max-height: 33px; min-height: 33px; width: 100%; color: rgb(100, 116, 139); padding: 0px 0px 0px 16px; background-color: rgb(248, 250, 252); border-bottom: 1px solid rgb(224, 224, 224); box-shadow: unset; border-radius: 0px;">
                        <v-card-text style="font-size: 0.875rem; padding-top: 4px; padding-left: 0px; margin-left: 0px;color: rgb(100, 116, 139);">
                            {{headline}}
                        </v-card-text>
                    </v-card>
                    <v-card style="max-height: 55px; min-height: 55px; border-radius: 0px;">
                        <v-select :items="items" v-model="selected" style="width: 180px; margin-left: 12px"/>
                    </v-card>
                </v-card>   
            </div>
        </template>
        '''

    def __init__(
        self, 
        items:list = [], 
        style:str = '',
        headline:str = '',
        *args, 
        **kwargs
    ):
        super().__init__(*args, **kwargs)
        self.items=items
        self.style=style
        self.headline=headline

class SettingsPartsOptions():
    def __init__(
        self, 
        app_context, 
        context_key,
        data,
        minrowlange,
        columnChoices,
        *args,
        **kwargs
    ):
        super().__init__(*args, **kwargs)
        self.app_context=app_context 
        self.context_key=context_key
        self.data=data
        self.minrowlange=minrowlange
        self.columnChoices=columnChoices

        self.run_button = v.Col(
            children= [
                v.Btn(
                    style_ = "",
                    children = ['조회하기'],
                    rounded = True,
                    depressed = True,
                    dark = True,
                ),
            ],
            style_ = "margin:0; padding:0; display:flex; flex-direction:row; justify-content:flex-end; align-items:center; width:210px;",
        )
        # data range selector
        default = 1000 if len(self.data) / 2  > 1000 else len(self.data) / 2

        self.data_range_selector = get_or_create_class(
            'simple_slider_card',
            self.app_context,
            context_key = f'{self.context_key}__data_range_selector', 
            title = '행 범위',
            range = [1, len(self.data), 1, default],
            size = {'width':'210px', 'height':'90px'},
            style = 'background-color:#ffffff; border-bottom:1px solid #e0e0e0;',
        )

        # column selection
        df_col_names = pd.DataFrame(self.columnChoices, columns=['col_names'])

        self.column_selector = get_or_create_class(
            'select_table_card',
            self.app_context,
            context_key = f'{self.context_key}__column_selector', # tabular_analytics_basicinfo__column_selector
            title = '변수 선택',
            data = df_col_names,
            size = {'width':'210px', 'height':'200px'},
            style = 'background-color:#ffffff; border-bottom:1px solid #e0e0e0;',
        )

        # 색상 설렉터 정의
        self.color_option_selector = DataSelect(
            label = "Color",
            index = 0,
            items = color_options,
            v_model = None,
            dense = False,
            style_ = "max-width:250px; margin-left:0px;margin-right:0px; align-items: left;margin-top: 2px; ",
            readonly = False,
            autofocus = True,
        )

        # 설렉터 모음 딕셔너리 생성
        selector_names =["컬럼 선택","Hue 선택"]
        self.selector_dict= {}
        for selector_name in selector_names:
            s=SelectorCard(
                index=0,
                items=self.columnChoices,
                v_model=None,
                _style="width: 350px;",
                #color="#F8F8F8",
                headline=selector_name
            )

            self.selector_dict[selector_name]=s
        self.options_list=[]

class MultiSelector(v.VuetifyTemplate):
    items = traitlets.List([]).tag(sync=True, allow_null=True)  
    selected = traitlets.List([]).tag(sync=True)
    style = traitlets.Unicode(default_value=None, allow_none=True).tag(sync=True)

    @traitlets.default('template')
    def _template(self):
        return '''
        <template>
            <div>
                <v-select :items="items" multiple v-model="selected"
                :style="style"/>
            </div>
        </template>
        '''

    def __init__(
        self, 
        items:list = [], 
        style:str = '',
        *args, 
        **kwargs
    ):
        super().__init__(*args, **kwargs)
        self.items=items
        self.style=style



