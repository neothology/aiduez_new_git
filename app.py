from models.context import AppContext
from utils import get_or_create_class
class Aian:
    def __init__(self, **kwargs):

        # iniitalize app context (model)
        self.app_context = AppContext(
            theme = kwargs.get('theme') if kwargs.get('theme') else 'ez_default',
        ) 

        # initialize layout
        self.alert = get_or_create_class('alert', self.app_context)
        self.base_overlay = get_or_create_class('base_overlay', self.app_context)
        self.background = get_or_create_class('background', self.app_context)
        self.top_area = get_or_create_class('top_area', self.app_context)
        self.page_progress = get_or_create_class('progress_linear', self.app_context, style = 'position:absolute; top:200px; z-index:780;')
        self.work_area = get_or_create_class('work_area', self.app_context)
        self.side_nav = get_or_create_class('side_nav', self.app_context)

        # initialize components
        self.side_nav_menu = get_or_create_class('list_menu', self.app_context, context_key='side_nav_menu') # use context_key when context key differs from class name

        # merge components into layouts
        self.side_nav.children = [self.side_nav_menu]
        self.background.children = [self.alert, self.base_overlay, self.top_area, self.page_progress, self.side_nav, self.work_area]
        # self.background.children = [self.alert, self.top_area, self.page_progress, self.side_nav, self.work_area]

    def start(self):
        return self.background

