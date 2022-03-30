import os
import re
import zipfile
import ipyvuetify as v
from utils import get_or_create_class, delete_files_in_dir
from utils import logging_time
from components.upload.upload_widgets import UploadWidgets


class TabularWorkbook:
    def __init__(self, app_context, context_key:str = ""):
        self.app_context = app_context
        self.context_key = context_key
        self.workspace_dir = self.app_context.env_values['workspace_dir']
        self.tmp_dir = app_context.env_values['tmp_dir']
        self.tmp_workbook_dir = f'{self.tmp_dir}/workbook'
        self.tmp_works_dir = f'{self.tmp_workbook_dir}/works'
        self.workbook_name = ''
        self.workbook_path = ''
        self.work_name_list = []
        self.work_dir_list = []
        self.current_work_name: str = ''
        self.current_data_column = []
        self.current_work_dir: str = ''
        self.current_work_state_dir: str = ''
        self.current_models_dir: str = ''
       
        
    def create_new(self):

        # make 'workbook' directory in 'tmp' directory
        if os.path.exists(self.tmp_workbook_dir): # /aihub/workspace/tmp/workbook
            delete_files_in_dir(self.tmp_workbook_dir)
        else:
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
        
        self.workbook_name = _generate_workbook_name(self.workspace_dir) 
        self.workbook_path = f'{self.workspace_dir}/{self.workbook_name}'
        zipfile.ZipFile(self.workbook_path, 'w').close() # e.g. /aihub/workspace/Untitled.ezx

    def create_new_work(self, work_name, data):

        def _check_work_name(work_name:str):

            # (1) 첫글자는 영문 또는 한글만 (2) 특수문자는 '_' 만 가능, 
            chk_all = re.compile('[^a-zA-Z0-9ㄱ-ㅎ가-힣_]')
            chk_first = re.compile('[a-zA-Zㄱ-ㅎ가-힣]')
            
            if chk_first.match(work_name) is None:
                raise Exception('데이터 이름은 영문 또는 한글로 시작해야 합니다.')
            elif chk_all.search(work_name) is not None:
                raise Exception("데이터 이름은 영문, 숫자, 한글, 그리고 '_'만 가능합니다.")

            # check if data name already exists
            if work_name in self.work_name_list:
                raise Exception(f'{work_name}이/가 이미 존재합니다.')

            return work_name

        # def _check_data_column(data):

        #     # Column명은 영문이랑 '_'만 허용
        #     chk_col_all = re.compile('[^a-zA-Z0-9_]')
        #     column_list = data.columns.tolist()

        #     for i in range(0, len(column_list)):
        #         if chk_col_all.search(column_list[i]) is not None:
        #             raise Exception("데이터 컬러명은 영문, 숫자, 그리고 '_'만 가능합니다. ")
            
        #     return data

            

        # make work directory
        self.current_work_name = _check_work_name(work_name) # e.g. 'titanic_train'
        # self.current_data_column = _check_data_column(data)
        self.current_work_dir = f'{self.tmp_works_dir}/{work_name}'  # e.g. /aihub/workspace/tmp/workbook/works/titanic_train
        os.makedirs(self.current_work_dir)

        # make work_state directory
        self.current_work_state_dir = f'{self.current_work_dir}/work_state'
        os.makedirs(self.current_work_state_dir)

        # make models directory
        self.current_models_dir = f'{self.current_work_dir}/models' # e.g. /aihub/workspace/tmp/workbook/works/titanic_train/models
        os.makedirs(self.current_models_dir)

        # invoke dataset object and add data to it
        self.dataset = get_or_create_class('tabular_dataset', self.app_context)
        self.dataset.add_data(self.current_work_name, data, self.current_work_dir)

        self.work_name_list.append(work_name)
        self.work_dir_list.append(self.current_work_dir)

    def save_current_work(self):
        # save current work -(1) 데이터 입수
        # save current work -(2) 데이터 분석
        # self.app_context.current_workflow_stage_sub
        # save current work -(3) 데이터 가공
        # save current work -(4) AI모델 학습(모델관련 내용은 '학습'할 때 저장되므로 여기서는 training options 만 저장)
        self.app_context.tabular_ai_training__training_options.save_config(self.current_work_state_dir)
        # save current work -(5) AI모델 평가


    def load_existing_work(self, work_name):

        # work 변경
        self.current_work_name = work_name
        self.current_work_dir = f'{self.tmp_works_dir}/{work_name}'
        self.current_work_state_dir = f'{self.current_work_dir}/work_state'

        # data 변경
        self.app_context.tabular_dataset.change_data_to(work_name, self.current_work_dir)

        # analytics 변경
        if self.app_context.tabular_data_analytics__options:
            self.app_context.tabular_contents_sub.children = []
            self.app_context.tabular_data_analytics__options = None
            self.app_context.tabular_data_analytics__sub_menu.last_activated_item.class_list.remove("now_active")
            self.app_context.tabular_data_analytics__sub_menu.last_activated_item = None
        if self.app_context.tabular_analytics_basicinfo:
            self.app_context.tabular_analytics_basicinfo__column_selector = None
            self.app_context.tabular_analytics_basicinfo__data_range_selector = None
            self.app_context.tabular_analytics_basicinfo = None

        self.app_context.progress_overlay.update(20)

        # training 변경
        tabular_ai_training = get_or_create_class('tabular_ai_training', self.app_context)
        
        tabular_ai_training.train_button.disabled = True

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
        self.app_context.progress_overlay.start()
        self.save_current_work()
        self.load_existing_work(work_name)
        self.app_context.progress_overlay.finish()

    def save_current_work_as(self, work_name):
        pass

    def save_workbook():
        pass

    def save_workbook_as():
        pass

    def rename_workbook():
        pass
