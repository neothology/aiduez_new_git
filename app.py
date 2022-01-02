from dacite import from_dict
from config import AppConfig
from context import AppContext
from utils import read_config, get_or_create_class

class Aian:
    def __init__(self):

        # read config file, convert to dict and then to AppConfig
        self.app_config = from_dict(data_class = AppConfig, data = read_config())

        # initialize AppContext
        self.app_context = AppContext()

        # initialize layout
        self.background = get_or_create_class('background', self.app_context, self.app_config)
        self.top_area = get_or_create_class('top_area', self.app_context, self.app_config) 
        self.work_area = get_or_create_class('work_area', self.app_context, self.app_config)
        self.side_nav = get_or_create_class('side_nav', self.app_context, self.app_config)
        self.top_area = get_or_create_class('top_area', self.app_context, self.app_config) 

        # initialize components
        self.side_nav_menu = get_or_create_class('list_menu', self.app_context, self.app_config, key='side_nav_menu')

        # merge components into layouts
        self.side_nav.children = [self.side_nav_menu]
        self.background.children = [self.top_area, self.work_area, self.side_nav]

        # when re-loaded, establish from thst last saved state
        # ...


    def start(self):
        return self.background

