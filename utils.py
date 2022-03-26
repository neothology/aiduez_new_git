import yaml
from os.path import expanduser
import importlib
import shutil
import os
import json
import numpy as np


def read_config():
    path = f'{expanduser("~")}/.aiduez/aiduez_config.yml'
    with open(path, 'r') as stream:
        try:
            return yaml.safe_load(stream)
        except yaml.YAMLError as exc:
            # print(exc)
            pass

# return component class if exist, else init a new component class, keep it in the context if needed, and return it
def get_or_create_class(class_path_key:str, app_context:object, context_key:str = None, update:bool = False, **kwargs):
    class_path = app_context.class_paths.get(class_path_key)
    module_path = '.'.join(class_path.split('.')[:-1])
    class_name = class_path.split('.')[-1]
    if not context_key:
            context_key = class_path_key
    if not update:
        try:
            if not getattr(app_context, context_key): # if None in app_context with the context_key
                imported_class = getattr(importlib.import_module(module_path), class_name)
                class_instance = imported_class(app_context, context_key,  **kwargs)
                setattr(app_context, context_key, class_instance)
            else:
                class_instance = getattr(app_context, context_key)
        except (AttributeError, TypeError): # when no class_name in app_context
            # print(f"no context key for {context_key}")
            imported_class = getattr(importlib.import_module(module_path), class_name)
            class_instance = imported_class(app_context, context_key, **kwargs)
    else:
        imported_class = getattr(importlib.import_module(module_path), class_name)
        class_instance = imported_class(app_context, context_key,  **kwargs)
        setattr(app_context, context_key, class_instance)

    return class_instance   

def set_theme_style(app_context: dict, context_key: str,  elem: str = 'base', style_type: str = 'default') -> dict:
    return app_context.theme_values[context_key]['style'][elem][style_type] 

def delete_files_in_dir(dir_path, except_files: list = []):
    for filename in os.listdir(dir_path):
        if filename not in except_files:
            file_path = os.path.join(dir_path, filename)
            try:
                if os.path.isfile(file_path) or os.path.islink(file_path):
                    os.unlink(file_path)
                elif os.path.isdir(file_path):
                    shutil.rmtree(file_path)
            except Exception as e:
                print('Failed to delete %s. Reason: %s' % (file_path, e))

class JsonEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, np.integer):
            return int(obj)
        elif isinstance(obj, np.floating):
            return float(obj)
        elif isinstance(obj, np.ndarray):
            return obj.tolist()
        else:
            return super(JsonEncoder, self).default(obj)

def get_dataset_stat(df):
    num_of_obs, num_of_var = df.shape
    num_of_missing_cells = df.isna().sum().sum()

    f2 = lambda x: float(int(x * 1000))/1000

    ratio_of_missing_cells = f2(num_of_missing_cells / (num_of_obs * num_of_var) * 100)
    num_of_duplicated = df.duplicated().sum()
    ratio_of_duplicated = f2(num_of_duplicated / num_of_obs * 100)

    return {
        'Number of variables': num_of_var, 'Number of observations': num_of_obs,
        'Missing cells': num_of_missing_cells, 'Missing cells(%)': ratio_of_missing_cells,
        'Duplicated rows': num_of_duplicated, 'Duplicated rows(%)': ratio_of_duplicated
    }

def get_variable_types(df):
    variable_types = {'Numeric': np.number,
                     'Object': 'object', 'Category': 'category',
                     'Datetime': 'datetime', 'Timedeltas': 'timedelta'}
    return {k: len(df.select_dtypes(include=v).columns) for k, v in variable_types.items()}