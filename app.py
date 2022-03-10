from context import AppContext
from utils import read_config, get_or_create_class

class Aian:
    def __init__(self, **kwargs):

        # iniitalize app context (app_config will be loaded from aiduez_config.yml during initialization)
        self.app_context = AppContext(
            theme = kwargs.get('theme') if kwargs.get('theme') else 'ez_default',
        ) 
        
        # initialize layout
        self.background = get_or_create_class('background', self.app_context)
        self.top_area = get_or_create_class('top_area', self.app_context)
        self.work_area = get_or_create_class('work_area', self.app_context)
        self.side_nav = get_or_create_class('side_nav', self.app_context)
        self.top_area = get_or_create_class('top_area', self.app_context) 

        # initialize components
        self.side_nav_menu = get_or_create_class('list_menu', self.app_context, context_key='side_nav_menu') # use context_key when context key differs from class name

        # merge components into layouts
        self.side_nav.children = [self.side_nav_menu]
        self.background.children = [self.top_area, self.side_nav, self.work_area]

        # when re-loaded, establish from thst last saved state
        # ...


    def start(self):
        return self.background

