import ipyvuetify as v
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

        # initialize layout and components
        self.background = get_or_create_class(self.app_config.class_path['BackGround'], self.app_context, self.app_config)
        self.work_area = get_or_create_class(self.app_config.class_path['WorkArea'], self.app_context, self.app_config)
        self.side_nav = get_or_create_class(self.app_config.class_path['SideNav'], self.app_context, self.app_config)
        self.list_menu = get_or_create_class(self.app_config.class_path['ListMenu'], self.app_context, self.app_config)
        self.top_area = get_or_create_class(self.app_config.class_path['TopArea'], self.app_context, self.app_config) # TopArea must be last to be initialized

        # merge layout components into background
        self.side_nav.children = [self.list_menu]
    
        self.background.children = [self.top_area, self.work_area, self.side_nav]

        # when re-loaded, establish from thst last saved state
        # ...


    def start(self):
        return self.background

