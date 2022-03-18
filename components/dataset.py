import ipyvuetify as v
import os
import pandas as pd
from pathlib import Path

class TabularDataset:

    def __init__(self, app_context:object = None, context_key:str = '', **kwargs):
        self.app_context = app_context
        self.context_key = context_key

        self.data_name_list = []
        self.data_path_list = []

        self.dataset_dir = self.app_context.pipeline.tmp_dir_data

        # code will be removed: load data form /aihub/workspace/temp/data/
        self.data_name_list = [Path(data_name).stem for data_name in sorted(os.listdir(self.dataset_dir))]
        self.data_path_list = [os.path.join(self.dataset_dir, f'{data_name}.csv') for data_name in self.data_name_list]
        self.current_data_name = self.data_name_list[2]
        self.current_data = pd.read_csv(self.data_path_list[2], sep = ',', encoding = 'cp949')

    # add loaded data to /aihub/workspace/temp/data/
    def add_data(self, data_name:str, data:pd.DataFrame):
        data_name_stem = Path(data_name).stem
        data_path = os.path.join(self.dataset_dir,  f'{data_name_stem}.csv')
        data.to_csv(os.path.join(data_path, data_name_stem), sep = ',', index = False, encoding = 'cp949')
        self.data_name_list.append(data_name)
        self.data_path_list.append(data_path)

        # set added data to current data
        self.current_data = data
        self.current_data_name = data_name_stem

    def load_data(self, data_name:str):
        data_index = self.data_name_list.index(data_name)
        return pd.read_csv(self.data_path_list[data_index], sep = ',', encoding = 'cp949')

    def select_current_data(self, data_name:str):
        self.current_data = self.load_data(data_name)
        self.current_data_name = data_name
        

class TabularDataContext(v.Row):
    def __init__(self, app_context:object = None, context_key:str = '', **kwargs):
        self.app_context = app_context
        self.context_key = context_key
        self.dataset = self.app_context.tabular_dataset
        self.data_name_list = self.dataset.data_name_list
        self.current_data_name = self.dataset.current_data_name

        self.style = {
            'row': 'width:1570px; align-self:center;',
            'data_selector': 'max-width:400px;',
        }

        self.data_selector = v.Select(
            v_model = self.current_data_name,
            items = self.data_name_list,
            dense = True,
            filled = True,
            label = '학습 데이터 선택',
            class_ = "tabula-data-selector",
            style_ = self.style['data_selector'],
        )

        def _on_data_selector_change(item, event=None, data=None):
            self.data_selector.v_model = item
            self.dataset.select_current_data(item)

        self.data_selector.on_event('change', _on_data_selector_change)

        super().__init__(
            style_ = self.style['row'],
            children = [self.data_selector],
        )

