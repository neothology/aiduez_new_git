from pathlib import Path
import os
def make_path_select_options(data_path, recursive = False, extensions = None):
    if recursive:
        if extensions is None:
            return [(file_name,Path(dir_path, file_name)) for dir_path, dir_names, file_names in os.walk(data_path) for file_name in file_names]
        else:
            return [(file_name,Path(dir_path, file_name)) for dir_path, dir_names, file_names in os.walk(data_path) for file_name in file_names if os.path.splitext(file_name)[-1] in extensions]
    else:
        if extensions is None:
            return [(file_name,Path(data_path,file_name)) for file_name in os.listdir(data_path) if os.path.isfile(file_name)]
        else:
            return [(file_name,Path(data_path,file_name)) for file_name in os.listdir(data_path) if os.path.isfile(file_name) and os.path.splitext(file_name)[-1] in extensions]
def make_backtick_name(name):
    if name.isnumeric():
        return "`" + name + "`"
    else:
        return name
