from utils import get_or_create_class
import numpy as np
import pandas as pd

class TabularAnalyticsBase:
    def __init__(self, app_context, context_key, target_view_name, **kwargs):
        self.app_context = app_context
        self.context_key = context_key
        self.target_view_name = target_view_name

        self.target_area = get_or_create_class('sub_area', self.app_context, 'tabular_data_analytics__sub_contents') 
        self.data = self.app_context.tabular_dataset.current_data

    def show_contents(self):
        self.view_instance.show()

class TabularaAnalyticsBasicinfo(TabularAnalyticsBase):
    def __init__(self, app_context, context_key, **kwargs):
        self.app_context = app_context
        self.context_key = context_key
        self.target_view_name = 'tabular_analytics_basicinfo_view'
        super().__init__(self.app_context, self.context_key, self.target_view_name, **kwargs)

        # make setting data:
        self.x_cols = pd.DataFrame(self.data.columns, columns=['col_names'])
        self.data_range_default = len(self.data) // 2 if len(self.data) // 2 <= 1000 else 1000
        
        self.view_instance = get_or_create_class(
            self.target_view_name, 
            self.app_context, 
            target_area = self.target_area,
            x_cols = self.x_cols,
            data_range = [1, len(self.data), 1, self.data_range_default],
        )

class TabularAnalyticsScatter(TabularAnalyticsBase):
    def __init__(self, app_context, context_key, **kwargs):
        self.app_context = app_context
        self.context_key = context_key
        self.target_view_name = 'tabular_analytics_scatter_view'
        super().__init__(self.app_context, self.context_key, self.target_view_name, **kwargs)
       
       # make setting data:
        self.x_cols = pd.DataFrame(self.data.select_dtypes(include = [np.number]).columns, columns = ['col_name'])
        self.hue_cols = pd.DataFrame([col for col in self.data.columns.values if len(self.data[col].unique()) < 100], columns = ['col_name'])

        if len(self.data) <= 100:
            self.data_range_start = self.data_range_default = len(self.data) 
        elif len(self.data) <= 200:
            self.data_range_start = self.data_range_default = 100

        elif len(self.data) <= 2000:
            self.data_range_start = 100
            self.data_range_default = len(self.data) // 2
        else:
            self.data_range_start = 100
            self.data_range_default = 1000

        self.view_instance = get_or_create_class(
            self.target_view_name, 
            self.app_context, 
            target_area = self.target_area,
            x_cols = self.x_cols,
            hue_cols = self.hue_cols,
            data_range = [self.data_range_start, len(self.data), 1, self.data_range_default],
        )

class TabularAnalyticsHeatmap(TabularAnalyticsBase):
    def __init__(self, app_context, context_key, **kwargs):
        self.app_context = app_context
        self.context_key = context_key
        self.target_view_name = 'tabular_analytics_heatmap_view'
        super().__init__(self.app_context, self.context_key, self.target_view_name, **kwargs)
       
       # make setting data:
        self.x_cols = pd.DataFrame(self.data.select_dtypes(include = [np.number]).columns, columns = ['col_name'])

        if len(self.data) <= 100:
            self.data_range_start = self.data_range_default = len(self.data) 
        elif len(self.data) <= 200:
            self.data_range_start = self.data_range_default = 100

        elif len(self.data) <= 2000:
            self.data_range_start = 100
            self.data_range_default = len(self.data) // 2
        else:
            self.data_range_start = 100
            self.data_range_default = 1000

        self.view_instance = get_or_create_class(
            self.target_view_name, 
            self.app_context, 
            target_area = self.target_area,
            x_cols = self.x_cols,
            data_range = [self.data_range_start, len(self.data), 1, self.data_range_default],
        )

class TabularAnalyticsBoxplot(TabularAnalyticsBase):
    def __init__(self, app_context, context_key, **kwargs):
        self.app_context = app_context
        self.context_key = context_key
        self.target_view_name = 'tabular_analytics_boxplot_view'
        super().__init__(self.app_context, self.context_key, self.target_view_name, **kwargs)
       
       # make setting data:
        self.x_cols = pd.DataFrame([col for col in self.data.columns.values if len(self.data[col].unique()) < 100], columns = ['col_name'])
        self.y_cols = pd.DataFrame(self.data.select_dtypes(include = [np.number]).columns, columns = ['col_name'])
        self.hue_cols = pd.DataFrame([col for col in self.data.columns.values if len(self.data[col].unique()) < 50], columns = ['col_name'])

        if len(self.data) <= 100:
            self.data_range_start = self.data_range_default = len(self.data) 
        elif len(self.data) <= 200:
            self.data_range_start = self.data_range_default = 100

        elif len(self.data) <= 2000:
            self.data_range_start = 100
            self.data_range_default = len(self.data) // 2
        else:
            self.data_range_start = 100
            self.data_range_default = 1000

        self.view_instance = get_or_create_class(
            self.target_view_name, 
            self.app_context, 
            target_area = self.target_area,
            x_cols = self.x_cols,
            y_cols = self.y_cols,
            hue_cols = self.hue_cols,
            data_range = [self.data_range_start, len(self.data), 1, self.data_range_default],
        )

class TabularAnalyticsDensity(TabularAnalyticsBase):
    def __init__(self, app_context, context_key, **kwargs):
        self.app_context = app_context
        self.context_key = context_key
        self.target_view_name = 'tabular_analytics_density_view'
        super().__init__(self.app_context, self.context_key, self.target_view_name, **kwargs)
       
       # make setting data:
        self.x_cols = pd.DataFrame(self.data.select_dtypes(include = [np.number]).columns, columns = ['col_name'])
        self.hue_cols = pd.DataFrame([col for col in self.data.columns.values if len(self.data[col].unique()) < 50], columns = ['col_name'])

        if len(self.data) <= 100:
            self.data_range_start = self.data_range_default = len(self.data) 
        elif len(self.data) <= 200:
            self.data_range_start = self.data_range_default = 100

        elif len(self.data) <= 2000:
            self.data_range_start = 100
            self.data_range_default = len(self.data) // 2
        else:
            self.data_range_start = 100
            self.data_range_default = 1000

        self.view_instance = get_or_create_class(
            self.target_view_name, 
            self.app_context, 
            target_area = self.target_area,
            x_cols = self.x_cols,
            hue_cols = self.hue_cols,
            data_range = [self.data_range_start, len(self.data), 1, self.data_range_default],
        )

class TabularAnalyticsWordCloud(TabularAnalyticsBase):
    def __init__(self, app_context, context_key, **kwargs):
        self.app_context = app_context
        self.context_key = context_key
        self.target_view_name = 'tabular_analytics_wcloud_view'
        super().__init__(self.app_context, self.context_key, self.target_view_name, **kwargs)

        # make setting data:
        self.x_cols = pd.DataFrame(self.data.select_dtypes(include = "object").columns, columns = ['col_name'])

        if len(self.data) <= 100:
            self.data_range_start = self.data_range_default = len(self.data) 
        elif len(self.data) <= 200:
            self.data_range_start = self.data_range_default = 100

        elif len(self.data) <= 2000:
            self.data_range_start = 100
            self.data_range_default = len(self.data) // 2
        else:
            self.data_range_start = 100
            self.data_range_default = 1000

        self.view_instance = get_or_create_class(
            self.target_view_name, 
            self.app_context, 
            target_area = self.target_area,
            x_cols = self.x_cols,
            data_range = [self.data_range_start, len(self.data), 1, self.data_range_default]
        )