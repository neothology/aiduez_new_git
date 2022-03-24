import ipyvuetify as v
import os
import pandas as pd
from pathlib import Path
import re

class TabularDataset:

    def __init__(self, app_context:object = None, context_key:str = '', **kwargs):
        self.app_context = app_context
        self.context_key = context_key
        self.tmp_dir = self.app_context.env_values['tmp_dir']
        self.data_name_list = []
        self.data_path_list = []
        self.current_data_name = ''
        self.current_data_path = ''
        self.current_data = None

    def read_data(self, data_name:str):
        data_path_index = self.data_name_list.index(data_name)
        return pd.read_json(self.data_path_list[data_path_index])

    def _set_current(self, data_name:str, data:pd.DataFrame, work_dir:str):
        self.current_data_name = data_name
        self.current_data_dir = f'{work_dir}/data'
        self.current_data_path = f'{self.current_data_dir}/{data_name}.json'
        self.current_data = data

    # add loaded data to /aihub/workspace/temp/data/
    def add_data(self, data_name:str, data:pd.DataFrame, work_dir:str):

        self._set_current(data_name, data, work_dir)

        if not os.path.exists(self.current_data_dir):
            os.makedirs(self.current_data_dir)

        # save data to the current_data_path
        self.current_data.to_json(self.current_data_path, force_ascii=False)

        # append added data name & path to list
        self.data_name_list.append(self.current_data_name)
        self.data_path_list.append(self.current_data_path)

    def change_data_to(self, data_name:str, work_dir:str): # e.g. work_dir:/aihub/workspace/tmp/workbook/works/titanic_train
        self.current_data_name = data_name
        self.current_data_dir = f'{work_dir}/data'
        self.current_data_path = f'{self.current_data_dir}/{data_name}.json'
        self.current_data = self.read_data(data_name)      

class TabularDataContext(v.Row):
    def __init__(self, app_context:object = None, context_key:str = '', **kwargs):
        self.app_context = app_context
        self.context_key = context_key

        self.workbook = self.app_context.tabular_workbook
        self.dataset = self.app_context.tabular_dataset

        self.data_name_list = self.dataset.data_name_list
        self.current_data_name = self.dataset.current_data_name

        self.style = {
            'row': 'width:1570px; align-self:center; border-bottom:1px solid rgb(203 203 203);',
            'data_selector': 'max-width:400px; padding-bottom:20px',
        }

        self.data_selector = v.Select(
            v_model = self.current_data_name,
            items = self.data_name_list,
            attach = True,
            dense = True,
            outlined = True,
            hide_details = True,
            class_ = "tabula-data-selector",
            style_ = self.style['data_selector'],
        )

        def _on_data_selector_change(item, event=None, data=None):
            self.workbook.change_work(item.v_model)

        self.data_selector.on_event('change', _on_data_selector_change)        

        super().__init__(
            style_ = self.style['row'],
            children = [self.data_selector],
        )