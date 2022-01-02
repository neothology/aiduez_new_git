import yaml
from os.path import expanduser
import importlib

def read_config():
    path = f'{expanduser("~")}/.aiduez/aiduez_config.yml'
    with open(path, 'r') as stream:
        try:
            return yaml.safe_load(stream)
        except yaml.YAMLError as exc:
            # print(exc)
            pass

# return component class if exist, else init a new component class, keep it in the context if needed, and return it
def get_or_create_class(class_path_key, app_context, app_config, **kwargs):
    class_path = app_config.class_paths[class_path_key]
    module_path = '.'.join(class_path.split('.')[:-1])
    class_name = class_path.split('.')[-1]
    context_key = kwargs.get('context_key') if kwargs.get('context_key') else class_path_key

    try:
        if not getattr(app_context, context_key): # if None in app_context with the context_key
            imported_class = getattr(importlib.import_module(module_path), class_name)
            class_instance = imported_class(app_context, app_config, **kwargs)
            setattr(app_context, context_key, class_instance)
        else:
            class_instance = getattr(app_context, context_key)
    except (AttributeError, TypeError): # when no class_name in app_context
        imported_class = getattr(importlib.import_module(module_path), class_name)
        class_instance = imported_class(app_context, app_config, **kwargs)

    return class_instance
