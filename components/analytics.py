from turtle import color
import pandas as pd
import ipyvuetify as v
from components.tables import SelectTable, MyDataTable
from components.layouts import OptionsLayout
from utils import get_or_create_class

class TabularaAnalyticsBasicinfo(v.Container):
    def _get_key_value_table_data_list(self, dics):
        temp =  []
        temp.extend((
            [{'value':key, 'style':''} for key in dics.keys()],
            [{'value':dics[key], 'style':'text-align:right'} for key in dics.keys()],
        ))
        return list(zip(*temp))

    def __init__(self, app_context, context_key, **kwargs):
        from common import pandas_explore as exp

        self.app_context = app_context
        self.context_key = context_key

        self.data = pd.DataFrame(self.app_context.tabular_dataset.current_data.columns, columns=['col_names'])

        self.column_selector = SelectTable(
            self.app_context,
            context_key = f'{self.context_key}__column_selector', # tabular_analytics_basicinfo__column_selector
            data = self.data,
            size = {'width':'150px', 'height':'200px'},
            style = 'background-color:red;',
        )
        dataset_stat = exp.get_dataset_stat(self.data)
        variable_types = exp.get_variable_types(self.data)

        table_data_list=[]
        table_data_list.append(self._get_key_value_table_data_list(dataset_stat))
        table_data_list.append(self._get_key_value_table_data_list(variable_types))

        table_headers=["Statistics/3","Variable Types/3"]
        
        dfhead = self.data.head().astype('str')

        headers=[
            {
                'text': colname,
                'value': colname
            } for colname in dfhead.columns
        ]
        headers=[]
        for colname in self.data.columns.to_list():
            dicElm={}
            dicElm['text']=colname
            dicElm['value']=colname
            headers.append(dicElm)

        self.setting_part = v.Row(
            style_ = "background-color:yellow;",
            children = 
                [self.column_selector]
            
        )

        self.output_part = v.Row(
            style_ = "background-color:green; height:300px;",
            children = [""],
        )

        super().__init__(
            style_ = "min-width:100%; min-height:100%; display:flex; flex-direction:column;",
            children = [self.setting_part, self.output_part],
        )

class TabularAnalyticsScatter(v.Container):
    def __init__(self, app_context, context_key, **kwargs):
        self.app_context = app_context
        self.context_key = context_key

        #self._layout=OptionsLayout()
        #print(self._layout)
        #print(dir(self._layout))
        self._layout=v.Row(
            children=[
                v.Col(
                    #cols=12, md=6,
                    cols="6", md="4",
                    children=[
                        v.Card(outlined=True,color="secondary")
                    ]
                ),
                v.Col(
                    #cols=12, md=6,
                    cols="12", md="8",
                    children=[
                        v.Card(outlined=True,color="secondary")
                    ]
                )
            ]
        ) 
        
        super().__init__(
            style_ = "min-width:100%; min-height:100%; display:flex; flex-direction:column;",
            children = [
                self._layout
            ]
        )

class TabularAnalyticsHeatmap(v.Container):
    def __init__(self, app_context, context_key, **kwargs):
        self.app_context = app_context
        self.context_key = context_key
        super().__init__(
            style_ = "min-width:100%; min-height:100%; display:flex; flex-direction:column;",
            children = [self.context_key]
        )

class TabularAnalyticsBoxplot(v.Container):
    def __init__(self, app_context, context_key, **kwargs):
        self.app_context = app_context
        self.context_key = context_key
        super().__init__(
            style_ = "min-width:100%; min-height:100%; display:flex; flex-direction:column;",
            children = [self.context_key]
        )

class TabularAnalyticsDensity(v.Container):
    def __init__(self, app_context, context_key, **kwargs):
        self.app_context = app_context
        self.context_key = context_key
        super().__init__(
            style_ = "min-width:100%; min-height:100%; display:flex; flex-direction:column;",
            children = [self.context_key]
        )

class TabularAnalyticsWordCloud(v.Container):
    def __init__(self, app_context, context_key, **kwargs):
        self.app_context = app_context
        self.context_key = context_key
        super().__init__(
            style_ = "min-width:100%; min-height:100%; display:flex; flex-direction:column;",
            children = [self.context_key]
        )

class TabularAnalyticsDimensionReduction(v.Container):
    def __init__(self, app_context, context_key, **kwargs):
        self.app_context = app_context
        self.context_key = context_key
        super().__init__(
            style_ = "min-width:100%; min-height:100%; display:flex; flex-direction:column;",
            children = [self.context_key]
        )

class TabularAnalyticsClustering(v.Container):
    def __init__(self, app_context, context_key, **kwargs):
        self.app_context = app_context
        self.context_key = context_key
        super().__init__(
            style_ = "min-width:100%; min-height:100%; display:flex; flex-direction:column;",
            children = [self.context_key]
        )

class TabularAnalyticsDataSample(v.Container):
    def __init__(self, app_context, context_key, **kwargs):
        self.app_context = app_context
        self.context_key = context_key
        super().__init__(
            style_ = "min-width:100%; min-height:100%; display:flex; flex-direction:column;",
            children = [self.context_key]
        )