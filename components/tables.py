import ipyvuetify as v
import traitlets
import pandas as pd
import json
      
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

class SelectTable(v.VuetifyTemplate):    
    headers = traitlets.List([]).tag(sync=True, allow_null=True)
    items = traitlets.List([]).tag(sync=True, allow_null=True)
    selected = traitlets.List([]).tag(sync=True, allow_null=True)
    index_col = traitlets.Unicode('').tag(sync=True)
    template = traitlets.Unicode('''
        <template>
            <v-data-table
                v-model="selected"
                :headers="headers"
                :items="items"
                :item-key="index_col"
                show-select
                dense
                hide-default-footer
            >
            </v-data-table>
        </template>
        ''').tag(sync=True)
    
    def __init__(
        self, 
        app_context:object = None, 
        context_key:str = "", 
        data=pd.DataFrame(),
        size:dict = {'width':'150px', 'height':'200px'},
        *args,
        **kwargs
        ):
        
        super().__init__(*args, **kwargs)
        
        self.app_context = app_context
        self.context_key = context_key
        data = data.reset_index()
        self.index_col = data.columns[0]
        self.style = kwargs.get('style', "") + f'width:{size["width"]}; height:{size["height"]};'
        
        headers = [{
              "text": col,
              "value": col
            } for col in data.columns]
        headers[0].update({'align': ' d-none'})
        headers[1].update({'text': ''})
        
        self.headers = headers        
        self.items = json.loads(
            data.to_json(orient='records'))