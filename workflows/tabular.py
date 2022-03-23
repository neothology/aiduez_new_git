import ipyvuetify as v
import os
import json
from utils import get_or_create_class
class TabularBase(v.Container):

    def __init__(self, app_context, context_key, **kwargs):
        self.app_context = app_context
        self.context_key = context_key
        self.tmp_workbook_dir = self.app_context.env_values['tmp_workbook_dir']

        # init workbook
        self.workbook = get_or_create_class('tabular_workbook', self.app_context)
        self.workbook.create_new() # tabular, text, image, video, audio, etc.

        # code will be removed: add data from /aihub/data to workbook data list---------
        from os import listdir, path
        import pandas as pd
        from pathlib import Path
        self.data_path_list = [path.join('data', data_name) for data_name in listdir('data')]

        for data_path in sorted(self.data_path_list):
            data = pd.read_csv(data_path, sep = ',', encoding = 'cp949')
            self.workbook.create_new_work(work_name = Path(data_path).stem, data = data)
        # ---------------------------------------------------------------

        # initialize components to view
        work_area_contents = get_or_create_class('sub_area', self.app_context, context_key = 'tabular_contents')

        self.tab_menu = get_or_create_class(
            'tab_menu', 
            self.app_context,  
            tab_props = self.app_context.workflows_list['tabular'],
            context_key = 'tabular_tab_menu',
            target_area = work_area_contents
            )

        # put components into layout
        super().__init__(
            style_ = "min-width:100%; min-height:100%;",
            children = [
                self.tab_menu, 
                work_area_contents,
                ],
        )

    def update_workflow_stages(self):
        pass

class TabularDataImport(v.Container):
    def __init__(self, app_context, context_key, **kwargs):
        self.app_context = app_context
        self.context_key = context_key

        self.import_tab = get_or_create_class(
            'tabular_data_import_tab',
            app_context = self.app_context,
            context_key = 'tabular_data_import_tab'
        )
        super().__init__(
            style_ = "min-width:100%; min-height:100%; display:flex; flex-direction:column",
            children = [
                self.import_tab,
                
            ],
        )

class TabularDataAnalytics(v.Container):
    def __init__(self, app_context, context_key, **kwargs):
        self.app_context = app_context
        self.context_key = context_key
        self.style = {}

        self.data = self.app_context.tabular_dataset.current_data

        # data_context
        self.data_context = get_or_create_class(
            'tabular_data_context',
            self.app_context,
            update = False,
        )

        self.sub_menu = get_or_create_class(
            'list_menu_sub',
            self.app_context,
            update = False
        )

        super().__init__(
            style_ = "min-width:100%; min-height:100%;",
            children = [
                self.data_context,
                self.sub_menu,
                ]
        )

class TabularDataProcessing(v.Container):
    def __init__(self, app_context, context_key, **kwargs):
        self.app_context = app_context
        self.context_key = context_key

        # vertical tab
        self.processing_tab = get_or_create_class(
            'tabular_data_processing_tab',
            app_context=self.app_context,
            context_key='tabular_data_processing_tab',
            update = True,
        )

        super().__init__(
            class_ = self.context_key,
            style_ = "min-width:100%; min-height:100%; display:flex; flex-direction:column;",
            children = [
                self.processing_tab,
            ],
        )

class TabularAITraining(v.Container):
    def __init__(self, app_context, context_key, **kwargs):
        self.app_context = app_context
        self.context_key = context_key
        self.style = {}

        self.data = self.app_context.tabular_dataset.current_data

        # data_context
        self.data_context = get_or_create_class(
            'tabular_data_context',
            self.app_context,
            update = False,
        )

        # model
        self.model = get_or_create_class(
            'tabular_model',
            self.app_context,
            update = True,
        )

        # train result
        self.train_result = get_or_create_class(
            'tabular_train_result',
            self.app_context,
            context_key = 'tabular_ai_training__train_result',
            update = True,
            title = '학습 로그',
            size = {'width':'90vw', 'height':'80vh'}, 
        )

        # train button
        self.train_button = get_or_create_class(
            'tabular_train_activator',
            self.app_context,
            context_key = 'tabular_ai_training__train_activator',
            update = True,
            title = '학습하기'
        )

        # training_options
        self.training_options = get_or_create_class(
            'tabular_training_options', 
            self.app_context, 
            context_key = 'tabular_ai_training__training_options',
            update = True,
            title = '학습 Parameter 설정',
        )

        # column summary
        initial_column_name = self.data.columns[0]
        self.column_summary = get_or_create_class(
            'column_summary',
            self.app_context,
            context_key = 'tabular_ai_training__column_summary',
            update = True,
            title = '데이터 요약',
            col = self.data[initial_column_name],
        )       

        super().__init__(
            class_ = self.context_key,
            style_ = "min-width:100%; min-height:100%; display:flex; flex-direction:column;",
            children = [
                self.data_context,
                v.Spacer(style_ = "height:20px"),
                self.train_button ,
                self.train_result,
                v.Spacer(style_ = "height:20px"),
                self.training_options,
                v.Spacer(style_ = "height:30px"),
                self.column_summary,
                v.Spacer(style_ = "height:30px"),
                ],
        )  

        self.app_context.tabular_ai_training__training_options.retrieve_training_options()
class TabularAIEvaluation(v.Container):
    def __init__(self, app_context, context_key, **kwargs):
        super().__init__(
            style_ = "min-width:100%; min-height:100%;",
            children = []
        )