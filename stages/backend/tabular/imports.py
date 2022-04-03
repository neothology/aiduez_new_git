from pathlib import Path

class FileObjectHandler:
    def __init__(self, app_context, context_key):
        self.app_context = app_context
        self.context_key = context_key
        self.file_object = None

    def load_data(self, item:object, encoding_option:str, delimiter_option:str):
        self.data_name = Path(item.get_files()[0]['name']).stem
        self.file_object = item.get_files()[0]['file_obj']
        self.file_object.seek(0)
        from io import StringIO
        import pandas as pd
        self.data = pd.read_csv(
            StringIO(
                self.file_object.read().decode(encoding_option)), 
                sep=delimiter_option
                )

        self.app_context.tabular_workbook.create_new_work(self.data_name, self.data)