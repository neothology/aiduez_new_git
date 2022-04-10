from utils import get_or_create_class
from glob import glob
from zipfile import ZipFile
import json

class TaskBase:
    def __init__(self, app_context:object, context_key:str, target_view_name:str, **kwargs):
        self.app_context = app_context
        self.context_key = context_key
        self.target_view_name = target_view_name
        self.workbook_profiles = []
        self.workbook_path_list = []
        self.workbook_name_list = []
        self.workspace_dir = self.app_context.env_values['workspace_dir']
        self.tmp_workbook_dir =f"{self.app_context.env_values['tmp_dir']}/workbook"

        self.workbook_card_data = []

    def _make_workbook_card_data(self, workbook_profile):
        import datetime
        created_at =  datetime.datetime.fromtimestamp(int(float(workbook_profile["created_at"]))).strftime('%Y-%m-%d')
        modified_at = datetime.datetime.fromtimestamp(int(float(workbook_profile["modified_at"]))).strftime('%Y-%m-%d')

        if len(workbook_profile["works"]) > 1:
            text = [
                f'{workbook_profile["works"][0]}등 {len(workbook_profile["works"])}개 데이터',
                f'생성:{created_at} / 변경:{modified_at}',
                ]
        elif len(workbook_profile["works"]) == 0:
            text = [
                '업로드된 데이터가 없습니다.',
                f'생성:{created_at} / 변경:{modified_at}',
                ]
        else:
            text = [
                f'{workbook_profile["works"][0]} 데이터',
                f'생성:{created_at} / 변경:{modified_at}',
                ]

        return {
            'workbook_type': workbook_profile['workbook_type'],
            'title': workbook_profile['name'],
            'workbook_icon': workbook_profile['workbook_icon'],
            'workbook_color': workbook_profile['workbook_color'],
            'favorite': workbook_profile['favorite'],
            'text': text
        }

    def load_workbook_profiles_and_show(self):
        self.workbook_profiles = []
        # gather workbook profiles in workspace
        self.workbook_path_list = glob(f'{self.workspace_dir}/*.ezx')
        if self.workbook_path_list:
            for workbook_path in self.workbook_path_list:
                with ZipFile(workbook_path) as workbook:    
                    with workbook.open('workbook_profile.json') as profile:
                        workbook_profile = json.loads(profile.read().decode('utf-8'))
                        import os
                        workbook_profile['name'] = os.path.basename(workbook_path)
                        self.workbook_profiles.append(workbook_profile)
                        self.workbook_name_list.append(os.path.basename(workbook_path))

        self.sorted_workbook_profiles = self.sort_workbook_profiles(self.workbook_profiles)
        self.workbook_card_data = [self._make_workbook_card_data(profile) for profile in self.sorted_workbook_profiles] # list of dict
        self.target_area = get_or_create_class(self.app_context.side_nav_menu_list['target_area'], self.app_context) # work_area  

        self.view_instance = get_or_create_class(
            self.target_view_name, # e.g.'task_recent_view
            self.app_context, 
            update = True,
            workbook_card_data = self.workbook_card_data 
        )

        self.app_context.current_workflow = 'task'
        self.view_instance.show(self.target_area)

    def load_workbook(self, workbook_type, workbook_name):

        import os
        from utils import delete_files_in_dir
        self.tmp_dir = self.app_context.env_values['tmp_dir']
        if os.path.exists(self.tmp_dir):
            delete_files_in_dir(self.tmp_dir)
        else:
            os.makedirs(self.tmp_dir)

        workbook_path = f'{self.workspace_dir}/{workbook_name}'
        with ZipFile(workbook_path) as workbook:
            workbook.extractall(self.tmp_workbook_dir)
        
        workflow_base = get_or_create_class(f'{workbook_type}_base', self.app_context) # e.g. 'tabular_base'
        workflow_base.load_workbook_from_tmp(workbook_name)
            
    def return_to_current_workflow_stage(self):
        workbook_type = self.app_context.current_workbook.flow_type
        workflow_base = get_or_create_class(f'{workbook_type}_base', self.app_context) # e.g. 'tabular_base'
        workflow_base.return_to_current_workflow_stage()

    def rename_workbook(self, selected_workbook_name, new_workbook_name):
        # check new name is valid
        from utils import check_string_validation_a
        _ = check_string_validation_a(new_workbook_name)

        #
        import shutil
        import os
        if os.path.exists(f'{self.workspace_dir}/{new_workbook_name}.ezx'):
            raise Exception(f'{new_workbook_name} 은 이미 존재하는 이름입니다.')

        shutil.move(os.path.join(self.workspace_dir, f'{selected_workbook_name}.ezx'), os.path.join(self.workspace_dir, f'{new_workbook_name}.ezx'))

        if self.app_context.current_workbook:
            if f'{selected_workbook_name}.ezx' == self.app_context.current_workbook.current_workbook_name:
                # workbook
                import time
                self.app_context.current_workbook.current_workbook_name = f'{new_workbook_name}.ezx'
                self.app_context.current_workbook.current_workbook_path = f'{self.workspace_dir}/{new_workbook_name}.ezx'
                self.app_context.current_workbook.profile['modified_at'] = str(time.time())
                self.app_context.save_workbook()

        # task: reload workbook profiles
        self.load_workbook_profiles_and_show()  

    def delete_workbook(self, workbook_full_name):

        import os
        os.remove(os.path.join(self.workspace_dir, workbook_full_name))

        self.load_workbook_profiles_and_show()  

    def check_active(self, workbook_full_name):
        if self.app_context.current_workbook:
            if  workbook_full_name == self.app_context.current_workbook.current_workbook_name:
                raise Exception('현재 열려 있는 Workbook을 삭제할 수 없습니다.')

class TaskRecent(TaskBase):
    def __init__(self, app_context:object, context_key:str, **kwargs):
        self.app_context = app_context
        self.context_key = context_key
        self.target_view_name = 'task_recent_view'

        super().__init__(
            self.app_context, 
            self.context_key, 
            self.target_view_name,
        )
    
    def sort_workbook_profiles(self, workbook_profiles):
        return sorted(workbook_profiles, key=lambda d: d['modified_at'], reverse=True)[:5]

class TaskFavorite(TaskBase):
    def __init__(self, app_context:object, context_key:str, **kwargs):
        self.app_context = app_context
        self.context_key = context_key
        self.target_view_name = 'task_favorite_view'

        super().__init__(
            self.app_context, 
            self.context_key, 
            self.target_view_name,
        )

    def sort_workbook_profiles(self, workbook_profiles):
        favorite_workbook_profiles = list(filter(lambda d: d['favorite'] == True, workbook_profiles))
        return sorted(favorite_workbook_profiles, key=lambda d: d['name'])

class TaskAll(TaskBase):
    def __init__(self, app_context:object, context_key:str, **kwargs):
        self.app_context = app_context
        self.context_key = context_key
        self.target_view_name = 'task_all_view'

        super().__init__(
            self.app_context, 
            self.context_key, 
            self.target_view_name,
        )

    def sort_workbook_profiles(self, workbook_profiles):
        return sorted(workbook_profiles, key=lambda d: d['name'])