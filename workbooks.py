import os
import re
import zipfile
import ipyvuetify as v
from utils import get_or_create_class, delete_files_in_dir, check_string_validation_a
import json
import time
import shutil

class TabularWorkbook:
    def __init__(self, app_context, context_key:str = ""):
        self.app_context = app_context
        self.context_key = context_key
        self.flow_type = 'tabular'
        self.workspace_dir = self.app_context.env_values['workspace_dir']
        self.tmp_dir = app_context.env_values['tmp_dir']
        self.tmp_workbook_dir = f'{self.tmp_dir}/workbook'
        self.tmp_works_dir = f'{self.tmp_workbook_dir}/works'
        self.work_name_list = []
        self.work_dir_list = []
        self.current_workbook_name = ''
        self.current_workbook_path = ''
        self.current_work_name: str = ''
        self.current_work_dir: str = ''
        self.current_work_state_dir: str = ''
        self.current_models_dir: str = ''
        self.dataset = None
        self.profile = None
       
        
    def create_new(self):

        # delete tmp directory contents if exists, else make tmp directory
        if os.path.exists(self.tmp_dir):
            delete_files_in_dir(self.tmp_dir)
        else:
            os.makedirs(self.tmp_dir)

        # make 'workbook' directory in 'tmp' directory
        os.mkdir(self.tmp_workbook_dir)

        # make 'Untitled.ezx' zipfile in 'workspace' directory
        def _generate_workbook_name(path):
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
        
        self.current_workbook_name = _generate_workbook_name(self.workspace_dir) 
        self.current_workbook_path = f'{self.workspace_dir}/{self.current_workbook_name}'
        zipfile.ZipFile(self.current_workbook_path, 'w').close() # e.g. /aihub/workspace/Untitled.ezx

        # initialize dataset object
        self.dataset = get_or_create_class('tabular_dataset', self.app_context, update=True)

        # create new workbook profile and save it
        import random
        icon_random = random.randint(0, 19)
        color_random = random.randint(0, 3)
        self.profile = {
            'workbook_type': 'tabular',
            'works': [],
            'models': [],
            'workbook_icon': self.app_context.workbook_icons[icon_random],
            'workbook_color': self.app_context.workbook_colors[color_random],
            'favorite': False,
            'description': '',
            'workflow_stage': self.app_context.current_workflow_stage,
            'current_work': '',
            'current_model': '',
            'created_at': str(time.time()),
            'modified_at': str(time.time()),
            'deleted_at': '',
        }

        with open(f'{self.tmp_workbook_dir}/workbook_profile.json', 'w') as f:
            json.dump(self.profile, f)

        self.save_workbook()

    def create_new_work(self, work_name, data):

        def _check_work_name(work_name:str):

            # check if work name is valid
            _ = check_string_validation_a(work_name)

            # check if data name already exists
            if work_name in self.work_name_list:
                raise Exception(f'{work_name}이/가 이미 존재합니다.')

            return work_name

        self.app_context.progress_linear.active = True

        # make work directory
        self.current_work_name = _check_work_name(work_name) # e.g. 'titanic_train'
        self.current_work_dir = f'{self.tmp_works_dir}/{work_name}'  # e.g. /aihub/workspace/tmp/workbook/works/titanic_train
        os.makedirs(self.current_work_dir)

        # make work_state directory
        self.current_work_state_dir = f'{self.current_work_dir}/work_state'
        os.makedirs(self.current_work_state_dir)

        # make models directory
        self.current_models_dir = f'{self.current_work_dir}/models' # e.g. /aihub/workspace/tmp/workbook/works/titanic_train/models
        os.makedirs(self.current_models_dir)

        # invoke dataset object and add data to it
        self.dataset.add_data(self.current_work_name, data)

        # self.work_name_list.append(work_name)
        self.work_dir_list.append(self.current_work_dir)

        # update 
        self.change_work(self.current_work_name)

        # update workbook profile
        self.save_workbook(work = self.current_work_name)

        self.app_context.progress_linear.active = False

    def save_workbook(self, **kwargs):

        self.app_context.progress_linear.active = True

        # save current work
        # save current work -(1) 데이터 입수
        # save current work -(2) 데이터 분석
        # self.app_context.current_workflow_stage_sub
        # save current work -(3) 데이터 가공
        # save current work -(4) AI모델 학습(모델관련 내용은 '학습'할 때 저장되므로 여기서는 training options 만 저장)
        if self.app_context.tabular_ai_training:
            self.app_context.tabular_ai_training__training_options.save_config(self.current_work_state_dir)
        # save current work -(5) AI모델 평가

        if kwargs.get('work'):
            if kwargs['work'] not in self.profile['works']:
                self.profile['works'].append(kwargs['work'])
            self.profile['current_work'] = kwargs['work']

        if kwargs.get('model'):
            if kwargs['model'] not in self.profile['models']:
                self.profile['models'].append(kwargs['model'])
            self.profile['current_model'] = kwargs['model']

        self.profile['workflow_stage'] = self.app_context.current_workflow_stage
        self.profile['modified_at'] = str(time.time())

        with open(f'{self.tmp_workbook_dir}/workbook_profile.json', 'w') as f:
            json.dump(self.profile, f)

        shutil.make_archive(f'{self.tmp_dir}/tmp_workbook', 'zip', self.tmp_workbook_dir)
        shutil.move(f'{self.tmp_dir}/tmp_workbook.zip', self.current_workbook_path)

        self.app_context.progress_linear.active = False

    def _load_existing_work(self, work_name):

        # work 변경
        self.current_work_name = work_name
        self.current_work_dir = f'{self.tmp_works_dir}/{work_name}'
        self.current_work_state_dir = f'{self.current_work_dir}/work_state'
        self.current_models_dir = f'{self.current_work_dir}/models'

        # data 변경
        self.app_context.tabular_dataset.change_data_to(work_name, self.current_work_dir)

        # analytics 변경

        if self.app_context.tabular_data_analytics:
            if self.app_context.tabular_data_analytics__options:
                self.app_context.tabular_data_analytics__sub_contents.children = []
                self.app_context.tabular_data_analytics__options = None
                self.app_context.tabular_data_analytics__sub_menu.last_activated_item.class_list.remove("now_active")
                self.app_context.tabular_data_analytics__sub_menu.last_activated_item = None
            if self.app_context.tabular_analytics_basicinfo:
                self.app_context.tabular_analytics_basicinfo__column_selector = None
                self.app_context.tabular_analytics_basicinfo__data_range_selector = None
                self.app_context.tabular_analytics_basicinfo = None
            if self.app_context.tabular_analytics_wcloud:
                self.app_context.tabular_analytics_wcloud__column_selector = None
                self.app_context.tabular_analytics_wcloud__data_range_selector = None
                self.app_context_tabular_analytics_wcloud = None


        # preprocessing 변경
        if self.app_context.tabular_data_processing:
            self.app_context.tabular_data_processing__sub_contents.children = []
            self.app_context.tabular_data_processing__options = None
            if self.app_context.tabular_data_processing__sub_menu.last_activated_item is not None:
                self.app_context.tabular_data_processing__sub_menu.last_activated_item.class_list.remove("now_active")
            self.app_context.tabular_data_processing__sub_menu.last_activated_item = None
            if self.app_context.tabular_data_single_processing is not None:
                self.app_context.tabular_data_single_processing.update()


        self.app_context.progress_overlay.update(20)

        # training 변경
        if self.app_context.tabular_ai_training:
            tabular_ai_training = get_or_create_class('tabular_ai_training', self.app_context)
            
            tabular_ai_training.train_button.children[2].disabled = True

            train_result = get_or_create_class(
                'tabular_train_result',
                self.app_context,
                context_key = 'tabular_ai_training__train_result',
                update = True,
                title = '학습 로그',
                size = {'width':'90vw', 'height':'80vh'}, 
            )
            
            self.app_context.progress_overlay.update(60)

            training_options = get_or_create_class(
                'tabular_training_options', 
                self.app_context, 
                context_key = 'tabular_ai_training__training_options',
                update = True,
                title = '학습 Parameter 설정',
            )

            self.app_context.progress_overlay.update(90)

            column_summary = get_or_create_class(
                'column_summary',
                self.app_context,
                context_key = 'tabular_ai_training__column_summary',
                update = True,
                title = '데이터 요약',
                col = self.app_context.tabular_dataset.current_data.iloc[:, 0],
            ) 

            self.app_context.progress_overlay.update(100)

            # hide show_result button
            self.app_context.tabular_ai_training__train_activator.show_result_btn.hide()

            tabular_ai_training.children = [
                tabular_ai_training.top_area,
                v.Spacer(style_ = "max-height:20px"),
                train_result,
                training_options,
                v.Spacer(style_ = "max-height:30px"),
                column_summary,
            ]
        
    def change_work(self, work_name):
        # self.app_context.progress_overlay.start()
        
        self.save_workbook()
        self._load_existing_work(work_name)
        self.save_workbook(work = work_name)


        self.app_context.progress_overlay.finish()

    def load_workbook_from_tmp(self, workbook_name):

        # load workbook profile
        with open(f'{self.tmp_workbook_dir}/workbook_profile.json', 'r') as f:
            self.profile = json.loads(f.read())

        self.work_name_list = self.profile['works']
        self.work_dir_list = [f'{self.tmp_works_dir}/{work_name}' for work_name in self.work_name_list]

        self.app_context.current_workflow_stage = self.profile['workflow_stage']

        # set workbook name
        self.current_workbook_name = workbook_name # e.g. 'Untitled.ezx'
        self.current_workbook_path = f'{self.workspace_dir}/{self.current_workbook_name}'

        # initialize dataset object
        self.dataset = get_or_create_class('tabular_dataset', self.app_context)
        self.dataset.data_name_list = self.work_name_list
        self.dataset.data_path_list = [f'{self.tmp_works_dir}/{work_name}/data/{work_name}.json' for work_name in self.work_name_list]

        # load saved work
        if self.profile['current_work']:
            self._load_existing_work(self.profile['current_work'])

        # update import view
        if self.app_context.tabular_data_import__workbook_data_list:
            self.app_context.tabular_data_import__workbook_data_list.update_data(self.app_context.tabular_dataset.data_name_list)

        # reset data context
        if self.app_context.tabular_data_context:
            self.app_context.tabular_data_context.reset()
