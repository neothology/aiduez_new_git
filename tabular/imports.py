from pathlib import Path
from utils import get_or_create_class

class TabularImportBase:
    def __init__(self, app_context, context_key, target_view_name, **kwargs):
        self.app_context = app_context
        self.context_key = context_key
        self.target_view_name = target_view_name

        self.target_area = get_or_create_class('sub_area', self.app_context, 'tabular_data_import__sub_contents')

    def show(self):
        if self.view_instance:
            self.view_instance.show()

    def _check_data_name(self, data_name):

        from utils import check_string_validation_a
        if not check_string_validation_a(self.app_context.snack_bar, data_name):
            return False

        if data_name in self.workbook_data_list:
            self.app_context.snack_bar.error(f'{data_name}이/가 이미 존재합니다.')
            return False

        self.app_context.snack_bar.release()
        return True

class TabularImportPC(TabularImportBase):
    def __init__(self, app_context, context_key, **kwargs):
        self.app_context = app_context
        self.context_key = context_key
        self.target_view_name = 'tabular_import_pc_view'
        super().__init__(self.app_context, self.context_key, self.target_view_name, **kwargs)

        self.workbook_data_list = self.app_context.tabular_dataset.data_name_list

        self.view_instance = get_or_create_class(
            self.target_view_name, 
            self.app_context, 
            target_area = self.target_area,
            workbook_data_list = self.workbook_data_list
        )

    def load_data(self, item:object, encoding_option:str, delimiter_option:str):
        self.data_name = Path(item.get_files()[0]['name']).stem

        if not self._check_data_name(self.data_name):
            return

        self.file_object = item.get_files()[0]['file_obj']
        self.file_object.seek(0)
        from io import StringIO
        import pandas as pd

        try:
            self.data = pd.read_csv(
                StringIO(
                    self.file_object.read().decode(encoding_option)), 
                    sep=delimiter_option
                    )
        except Exception as e:
            self.app_context.snack_bar.error(f'{e}')
            return

        self.app_context.snack_bar.release()
        self.app_context.current_workbook.create_new_work(self.data_name, self.data)
        self.view_instance.workbook_data_list_view.update(self.app_context.tabular_dataset.data_name_list)

class TabularImportAIDU(TabularImportBase):
    def _get_data_list_from_dir(self, dir):
        return [f.stem for f in Path(dir).iterdir() if f.is_file()], [f for f in Path(dir).iterdir() if f.is_file()]

    def __init__(self, app_context, context_key, **kwargs):
        self.app_context = app_context
        self.context_key = context_key
        self.target_view_name = 'tabular_import_aidu_view'
        super().__init__(self.app_context, self.context_key, self.target_view_name, **kwargs)

        self.workbook_data_list = self.app_context.tabular_dataset.data_name_list
        self.aidu_data_list, self.aidu_data_path_list = self._get_data_list_from_dir('/aihub/data/')

        self.view_instance = get_or_create_class(
            self.target_view_name, 
            self.app_context, 
            target_area = self.target_area,
            workbook_data_list = self.workbook_data_list,
            aidu_data_list = self.aidu_data_list
        )

    def load_data(self, index:str, encoding_option:str, delimiter_option:str):
        self.data_name = self.aidu_data_list[int(index)]

        if not self._check_data_name(self.data_name):
            return

        self.data_path = self.aidu_data_path_list[int(index)]
        import pandas as pd
        try:
            self.data = pd.read_csv(self.data_path, encoding= encoding_option, sep=delimiter_option)
        except Exception as e:
            self.app_context.snack_bar.error(f'{e}')
            return

        self.app_context.current_workbook.create_new_work(self.data_name, self.data)
        self.view_instance.workbook_data_list_view.update(self.app_context.tabular_dataset.data_name_list)


class TabularImportEDAP(TabularImportBase):
    # import pandas as pd
    # def __init__(self, app_context, context_key, **kwargs):
    #     self.app_context = app_context
    #     self.context_key = context_key
    #     self.target_view_name = 'tabular_import_edap_view'

    #     super().__init__(self.app_context, self.context_key, self.target_view_name, **kwargs)

    #     self.view_instance = get_or_create_class(
    #         self.target_view_name, 
    #         self.app_context, 
    #         target_area = self.target_area,
    #         database_list = [],
    #         table_list = []
    #     )
    # def load_data(self, data_name: str, data: pd.DataFrame):
    #     from io import StringIO
    #     self.data = data 
    #     self.data_name= data_name
    #     self.app_context.current_workbook.create_new_work(self.data_name, self.data)
    #     self.view_instance.workbook_data_list_view.update(self.app_context.tabular_dataset.data_name_list)
    def __init__(self, app_context, context_key, **kwargs):
        self.view_instance = None