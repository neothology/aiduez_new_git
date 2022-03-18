import os
import re
import zipfile
from distutils.dir_util import copy_tree
import pandas as pd
import mlflow as mf
from mlflow.tracking import MlflowClient
from utils import delete_files_in_dir

def generate_filename(path):
    files_only = [f for f in os.listdir(path) if os.path.isfile(os.path.join(path, f))] # file names only(not directories)
    match_result = [re.match('Untitled([1-9]\d*)[.]ezx|Untitled[.]ezx',name) for name in files_only] # match file names with 'Untitled~.ezx'
    file_no_list = [x.group(1) for x in match_result if x] # get file numbers including None('=Untitled.ezx')
    file_no_list_except_none = [int(y) for y in file_no_list if y]

    if None in file_no_list: # if 'Untitled.ezx' in files_only
        if len(file_no_list) == 1:
            return 'Untitled1.ezx'
        else:
            max_no = max(file_no_list_except_none)
            for i in range(1, max_no + 2):
                if i not in file_no_list_except_none:
                    return f'Untitled{i}.ezx'
    else:
        return 'Untitled.ezx'

class Pipeline:
    def __init__(self, app_context, context_key:str = ""):
        self.app_context = app_context
        self.context_key = context_key
        self.workspace_dir = self.app_context.env_values['workspace_dir']
        self.tmp_dir = self.app_context.env_values['tmp_dir']
        self.tmp_dir_data = os.path.join(self.tmp_dir, 'data')
        self.tmp_dir_models = os.path.join(self.tmp_dir, 'models')

    def create_new(self, task_type):

        # create new file(zip -> ezx) in workspace
        filename = generate_filename(self.workspace_dir)
        filepath = f'{self.workspace_dir}/{filename}'
        file = zipfile.ZipFile(filepath, 'w')

        # keep file object in context
        self.app_context.current_work_file = file

        # check whether 'tmp' exists and delete if it exists or create one
        if os.path.exists(self.tmp_dir):
            delete_files_in_dir(self.tmp_dir)
        else:
            os.mkdir(self.tmp_dir)

        # create data, model folder in tmp folder
        os.mkdir(self.tmp_dir_data)
        os.mkdir(self.tmp_dir_models)

        # code will be removed: temporary copy data to tmp folder
        copy_tree('data', self.tmp_dir_data)

        # create mlflow experiment in tmp folder (will be zipped later)
        mf_tracking_uri_base = os.path.join(self.tmp_dir, 'mf_tracking')
        mf_tracking_filename = filename.split('.')[0]
        os.makedirs(mf_tracking_uri_base)
        mf.set_tracking_uri(os.path.join(mf_tracking_uri_base, mf_tracking_filename))
        self.mf_client = MlflowClient()
        self.mf_client.create_experiment(mf_tracking_filename)
        self.app_context.mf_experiment_id = '1'
        self.app_context.mf_experiment_name = mf_tracking_filename

        # code_add: re-check whether (1) Untitled in workspace, (2) Untitled in tmp dir

    def load_data(self, data:pd.DataFrame):
        # load data to pipeline
        pass
        

