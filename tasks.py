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

    def _make_workbook_card_data(self, workbook_profile):
        import datetime
        created_at =  datetime.datetime.fromtimestamp(int(float(workbook_profile["created_at"]))).strftime('%Y-%m-%d %H:%M')
        modified_at = datetime.datetime.fromtimestamp(int(float(workbook_profile["modified_at"]))).strftime('%Y-%m-%d %H:%M')
        if len(workbook_profile["works"]) > 0:
            text = [
                f'{workbook_profile["works"][0]} 등, {len(workbook_profile["works"])}개 작업',
                f'생성:{created_at} / 변경:{modified_at}',
                ]
        else:
            text = [
                '0개의 작업',
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

    def load(self):
        self.workbook_profiles = []
        # gather workbook profiles in workspace
        self.workbook_path_list = glob(f'{self.app_context.env_values["workspace_dir"]}/*.ezx')
        if self.workbook_path_list:
            for workbook_path in self.workbook_path_list:
                with ZipFile(workbook_path) as workbook:
                    with workbook.open('workbook_profile.json') as profile:
                        self.workbook_profiles.append(json.loads(profile.read().decode('utf-8')))

        self.sorted_workbook_profiles = self.sort_workbook_profiles(self.workbook_profiles)
        self.workbook_card_data = [self._make_workbook_card_data(profile) for profile in self.sorted_workbook_profiles] # list of dict
        self.target_area = get_or_create_class(self.app_context.side_nav_menu_list['target_area'], self.app_context) # work_area    
        self.view_instance = get_or_create_class(
            self.target_view_name, # e.g.'task_recent_view
            self.app_context, 
            update = True,
            workbook_card_data = self.workbook_card_data 
        )
        self.view_instance.show(self.target_area)


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