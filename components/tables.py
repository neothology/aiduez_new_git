import ipyvuetify as v
import traitlets
import pandas as pd
import json
from components.cards import SimpleCard

class PlainTable(v.VuetifyTemplate):
    header = traitlets.Dict({}).tag(sync=True, allow_null=True)
    items = traitlets.List([]).tag(sync=True, allow_null=True)

    @traitlets.default('template')
    def _template(self):
        return '''
            <template>
                <v-simple-table light
                    style="margin-right:5px; border-radius:0; border-right:1px solid #e0e0e0; "
                >
                    <template v-slot:default>
                        <thead>
                            <tr style="height:33px; background-color:#f1f1f1;" >
                                <th 
                                    class="text-center"  
                                    style="height:33px; font-size: 0.875rem; font-weight:500; color: rgb(100, 116, 139);"        
                                    :colspan="header.colspan"
                                >
                                {{ header.text }}
                                </th>
                            </tr>
                        </thead>
                        <tbody>
                            <tr
                                v-for="item in items"
                                :key="item[0]"
                            >
                                <td
                                    v-for="elem in item"
                                    :style="elem.style"
                                >
                                {{ elem.value }}
                                </td>
                            </tr>
                        </tbody>
                    </template>
                </v-simple-table>
            </template>
        '''

    def __init__(
        self, 
        header:str = '', 
        items:list = [], 
        *args, 
        **kwargs
        ):

        super().__init__(*args, **kwargs)

        def _split_text_and_colspan(string:str):
          splited = string.split('/')
          return {'text':splited[0], 'colspan':splited[1]}
        self.header = _split_text_and_colspan(header)
        self.items = items

class SelectTableCard(SimpleCard): 
    def __init__(
        self, 
        app_context:object, 
        context_key:str, 
        title:str,
        data:pd.DataFrame(),
        size:dict = {},
        single_select:bool = False,
        **kwargs
    ):

        self.select_table = SelectTable(
            data = data,
            size = size,
            single_select = single_select,
            **kwargs,
        )

        super().__init__(
            class_ = context_key,
            title = title,
            body = self.select_table,
            size = {'width':size.get('width')},
            **kwargs,
        )

class SelectTable(v.VuetifyTemplate):    
    headers = traitlets.List([]).tag(sync=True, allow_null=True)
    items = traitlets.List([]).tag(sync=True, allow_null=True)
    single_select = traitlets.Bool(False).tag(sync=True)
    selected = traitlets.List([]).tag(sync=True, allow_null=True)
    index_col = traitlets.Unicode('').tag(sync=True)
    style = traitlets.Unicode('').tag(sync=True)
    template_with_header = traitlets.Unicode('''
            <template>
                <v-data-table
                    v-model="selected"
                    :headers="headers"
                    :items="items"
                    :item-key="index_col"
                    :style="style"
                    :items-per-page=-1
                    show-select
                    :single-select="single_select"
                    dense
                    hide-default-footer
                >
                </v-data-table>
            </template>
            ''').tag(sync=True)

    template_no_header = traitlets.Unicode('''
            <template>
                <v-data-table
                    v-model="selected"
                    :headers="headers"
                    :items="items"
                    :item-key="index_col"
                    :style="style"
                    :items-per-page=-1
                    show-select
                    :single-select="single_select"
                    dense
                    hide-default-header
                    hide-default-footer
                >
                </v-data-table>
            </template>
            ''').tag(sync=True)
            
    def __init__(
        self, 
        data=pd.DataFrame(),
        size:dict = {},
        single_select:bool = False,
        *args,
        **kwargs
        ):
        
        self.template = self.template_no_header if single_select else self.template_with_header
        self.headers = data.columns.tolist()
        self.items = data.to_dict('records')
        self.single_select = single_select
        self.selected = []
        self.index_col = 'id'
        self.style = ''
        self.size = size
        super().__init__(*args, **kwargs)
        super().__init__(*args, **kwargs)
        
        data = data.reset_index()
        self.index_col = data.columns[0]
        self.style = kwargs.get('style', "") + f'width:{size["width"]}; height:{size["height"]};' \
                     + "overflow-y:auto; overflow-x:hidden; font-weight:400;"
        self.single_select = single_select
        headers = [{
              "text": col,
              "value": col
            } for col in data.columns]
        headers[0].update({'align': ' d-none'})
        headers[1].update({'text': '(전체 선택)', 'sortable': False})
        
        self.headers = headers        
        self.items = json.loads(
            data.to_json(orient='records'))



class SelectTableCardNH(SimpleCard): 
    def _make_table(self, data, size):
        df = pd.DataFrame(data, columns = ['data_name']).iloc[:,0]
        return SelectTableNH(
            data = df,
            size = size,
        )

    def __init__(
        self, 
        app_context:object, 
        context_key:str, 
        title:str,
        data:list,
        size:dict = {},
        **kwargs
    ):
        self.app_context = app_context
        self.context_key = context_key
        self.title = title
        self.data = data
        self.size = size

        super().__init__(
            class_ = self.context_key,
            title = self.title,
            body = self._make_table(data, size),
            no_footer=True,
            size = {'width':self.size.get('width')},
            **kwargs,
        )
    
    def update_data(self, data):
        self.children[1].children = [self._make_table(data, self.size)]

class SelectTableNH(v.VuetifyTemplate):    
    headers = traitlets.List([]).tag(sync=True, allow_null=True)
    items = traitlets.List([]).tag(sync=True, allow_null=True)
    single_select = traitlets.Bool(False).tag(sync=True)
    selected = traitlets.List([]).tag(sync=True, allow_null=True)
    index_col = traitlets.Unicode('').tag(sync=True)
    style = traitlets.Unicode('').tag(sync=True)
    template = traitlets.Unicode('''
        <template>
            <v-data-table
                v-model="selected"
                :headers="headers"
                :items="items"
                :item-key="index_col"
                :style="style"
                :items-per-page=-1
                hide-default-header
                hide-default-footer
            >
            </v-data-table>
        </template>
        ''').tag(sync=True)
    
    def __init__(
        self, 
        data=pd.DataFrame(),
        size:dict = {},
        single_select:bool = False,
        *args,
        **kwargs
        ):
        
        super().__init__(*args, **kwargs)
        
        data = data.reset_index()
        self.index_col = data.columns[0]
        self.style = kwargs.get('style', "") + f'width:{size["width"]}; height:{size["height"]};' \
                     + "overflow-y:auto; overflow-x:hidden; font-weight:400;"
        self.single_select = single_select
        headers = [{
              "text": col,
              "value": col
            } for col in data.columns]
        headers[0].update({'align': ' d-none'})
        
        self.headers = headers        
        self.items = json.loads(
            data.to_json(orient='records'))
