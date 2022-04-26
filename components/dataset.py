import ipyvuetify as v
import os
import pandas as pd
from pathlib import Path
import re

class TabularDataset:

    def __init__(self, app_context:object = None, context_key:str = '', **kwargs):
        self.app_context = app_context
        self.context_key = context_key
        self.tmp_works_dir = self.app_context.current_workbook.tmp_works_dir
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
    def add_data(self, data_name:str, data:pd.DataFrame):
        
        work_dir = f'{self.tmp_works_dir}/{data_name}'
        self._set_current(data_name, data, work_dir)

        if not os.path.exists(self.current_data_dir):
            os.makedirs(self.current_data_dir)

        # save data to the current_data_path            
        self.current_data.to_json(self.current_data_path, force_ascii=False)

        # append added data name & path to list
        self.data_name_list.append(self.current_data_name)
        self.data_path_list.append(self.current_data_path)

        # reset data_context
        self.app_context.tabular_data_context.reset()

    def change_data_to(self, data_name:str, work_dir:str): # e.g. work_dir:/aihub/workspace/tmp/workbook/works/titanic_train
        self.current_data_name = data_name
        self.current_data_dir = f'{work_dir}/data'
        self.current_data_path = f'{self.current_data_dir}/{data_name}.json'
        self.current_data = self.read_data(data_name)      

class TabularDataContext(v.Col):
    def _make_data_selector(self):
        self.dataset = self.app_context.tabular_dataset
        self.data_name_list = self.dataset.data_name_list

        # raise Exception('add_data')
        self.current_data_name = self.dataset.current_data_name

        self.data_selector = v.Col(
            style_ = "padding:0; margin:0; max-width:50%;",
            children = [
                v.Select(
                    v_model = self.current_data_name,
                    items = self.data_name_list,
                    attach = True,
                    dense = True,
                    outlined = True,
                    hide_details = True,
                    class_ = "tabula-data-selector",
                    style_ = self.style['data_selector'],
                )
            ],
        )

        def _on_data_selector_change(item, event=None, data=None):
            self.app_context.base_overlay.start()  
            self.workbook = self.app_context.current_workbook
            self.workbook.change_work(item.v_model)
            self.app_context.base_overlay.stop()  

        self.data_selector.children[0].on_event('change', _on_data_selector_change)  

    def __init__(self, app_context:object = None, context_key:str = '', **kwargs):
        self.app_context = app_context
        self.context_key = context_key
        self.workbook = None
        self.data_selector = None
        self.style = {
            'col': 'max-height:60px; margin:0; padding:0; padding-top:10px; z-index:500;',
            'data_selector': 'max-width:400px; min-width:400px; padding-bottom:20px',
        }

        self._make_data_selector()     

        super().__init__(
            style_ = self.style['col'],
            children = [self.data_selector],
        )

    def reset(self):
        self._make_data_selector()
        self.children = [self.data_selector]
