import ipyvuetify as v
import traitlets

class SingleSelector(v.VuetifyTemplate):
    items = traitlets.List([]).tag(sync=True, allow_null=True)  
    selected = traitlets.List([]).tag(sync=True)
    style = traitlets.Unicode(default_value=None, allow_none=True).tag(sync=True)

    @traitlets.default('template')
    def _template(self):
        return '''
        <template>
            <div>
                <v-select :items="items" v-model="selected"
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

