import ipyvuetify as v
from utils import get_or_create_class


class TaskRecent(v.Container):
    def __init__(self, app_context, context_key, **kwargs):
        self.app_context = app_context
        self.context_key = context_key

        super().__init__(
            style_ = "min-width:100%; min-height:100%; padding-left:266px;",
            children = ['"최근 작업" - 화면/기능 개발 중...'],
        )

class TaskFavorite(v.Container):
    navigation_drawer_props = {'temporary':False, 'permanent':True, 'v_model':True}
    def __init__(self, app_context, context_key, **kwargs):
        self.app_context = app_context
        self.context_key = context_key

        super().__init__(
            style_ = "min-width:100%; min-height:100%; padding-left:266px;",
            children = ['"즐겨 찾기" - 화면/기능 개발 중...'],
        )

class TaskAll(v.Container):
    navigation_drawer_props = {'temporary':False, 'permanent':True, 'v_model':True}
    def __init__(self, app_context, context_key, **kwargs):
        self.app_context = app_context
        self.context_key = context_key
              
        super().__init__(
            style_ = "min-width:100%; min-height:100%; padding-left:266px;",
            children = ['"전체 작업" - 화면/기능 개발 중...'],
        )