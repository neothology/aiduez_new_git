import ipyvuetify as v
import traitlets
      
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

