from os import get_exec_path
import ipyvuetify as v
from utils import get_or_create_class
from components.tab import BaseTab
from components.cards import BaseCard, SimpleHeaderCard
from components.dialog import BaseDialog

######
# 버튼 생성 로직, 데이터 인코딩/구분자 선택 기능 모듈화 진행할 것!




class TabularImportTab(BaseTab):
    def __init__(self, app_context, context_key, **kwags) -> None:
        self.app_context = app_context
        # side tab
        tab_menus = []
        tab_items = []
        for stage in self.app_context.workflows_list['tabular']['stages']:
            if stage['title'] == "데이터 입수":
                for menu in stage['menu_list']:
                    tab_menus.append(menu["title"])
                    tab_items.append(menu["target"])
                break
            else:
                print("test")

        super().__init__(
            app_context=app_context,
            context_key=context_key,
            tab_menus=tab_menus,
            tab_items=tab_items,
            vertical=True,
            centered=True,
        )
class TabularAIDUImport(BaseCard):
    def __init__(self, app_context: object = None, context_key: str = "", title:str="", **kwargs):
        self.app_context = app_context
        self.context_key = context_key
        title = "AIDU에서 가져오기"
        
        
        self.data_upload = v.Container(
            children=[
                v.Row(
                    children=[
                        #데이터 조회
                        v.Col(
                            style_= 'font-size: 1rem; font-weight: bold; color; rgb(30, 41, 59);',
                            children=[
                                'AIDU 플랫폼에 업로드한 데이터',
                                v.Card(
                                    outlined = False,
                                    style_ = 'width: 800px; height:200px; overflow: auto;',
                                    children=[
                                        'Data will be fill in this place'
                                    ]
                                )
                            ]
                        ),
                        # 디자인 더미
                        v.Col(
                            children=[]
                        ),
                        # 인코딩
                        v.Col(
                            style_ = 'max-height: 15px; font-size: 1rem; font-weight: bold; color: rgb(30, 41, 59);',
                            children=[
                                '데이터 인코딩 선택',
                                v.RadioGroup(
                                    v_model = None,
                                    children=[
                                        v.Radio(label = 'UTF-8'),
                                        v.Radio(label = 'CP949(한글)'),
                                        v.Radio(label = 'EUC-KR(한글)')
                                    ]
                                )                                
                            ]
                        ),
                        # 구분자
                        v.Col(
                            style_= 'max-height: 15px; font-size: 1rem; font-weight: bold; color: rgb(30, 41, 59);',
                            children=[
                                '데이터 구분자',
                                v.RadioGroup(
                                    v_model = None,
                                    style_= 'font-size: 0.5rem;',
                                    children=[
                                        v.Radio(label = 'Comma: ","'),
                                        v.Radio(label = 'Tab: " "'),
                                        v.Radio(label = 'Pipe: "|"')
                                    ]
                                )
                            ]
                        )
                    ]
                ),
                v.Row(
                    style_ = 'padding-top: 15px',
                    children=[
                       
                        v.Layout(children = [
                            v.Spacer(),
                            v.Btn(color = 'primary', class_='ma-2 white--text', children = [
                                '데이터 가져오기',
                                v.Icon(right = True, children=['mdi-cloud-upload']),
                            ]),
                        ])
                    ]
                )
            ]
        )

        self.uploaded_data = v.Container(
            children=[
                v.Card(children = [
                    "Upload Data"
                ])
            ]
        )

        super().__init__(
            class_=context_key,
            header_title=title,
            
            body_items=[
                self.data_upload,
                self.uploaded_data

            ],
            body_size={
                "width": ["lg", "100px"],
                "height":["340px", "100px"],
            },
            body_border_bottom = [True, True],
            body_background_color = ["rgb(255, 255, 255)", "rgb(248, 250, 252)"],
            align='center'
        )

class TabularLocalImport(BaseCard):
    def __init__(self, app_context: object = None, context_key: str = "", title:str="", **kwargs):
        self.app_context = app_context
        self.context_key = context_key
        title = "PC에서 업로드하기"
        
        self.data_upload = v.Container(
            children=[
                v.Row(
                    children=[
                        # 인코딩
                        v.Col(
                            style_ = 'max-height: 15px; font-size: 1rem; font-weight: bold; color: rgb(30, 41, 59);',
                            children=[
                                '데이터 인코딩 선택',
                                v.RadioGroup(
                                    v_model = None,
                                    children=[
                                        v.Radio(label = 'UTF-8'),
                                        v.Radio(label = 'CP949(한글)'),
                                        v.Radio(label = 'EUC-KR(한글)'),
                                        v.Row(
                                            style_ = 'padding-top: 15px',
                                            children=[
                       
                                                v.Layout(children = [

                                                    v.Tooltip(right=True, v_slots =[{
                                                        'name': 'activator',
                                                        'variable': 'tooltip',
                                                        'children': v.Btn(v_on='tooltip.on', color = 'primary', class_='ma-2 white--text', children = [
                                                            'PC에서 업로드',
                                                            v.Icon(right = True, children = ['mdi-cloud-upload']),
                                                        ]),
                                                    }], children=[
                                                        'DRM 해제 문서만 업로드 가능'
                                                        ])
                            
                                                
                                            ])
                                            ]
                                        )
                                    ]
                                )                                
                            ]
                        ),
                        # 구분자
                        v.Col(
                            style_= 'max-height: 15px; font-size: 1rem; font-weight: bold; color: rgb(30, 41, 59);',
                            children=[
                                '데이터 구분자',
                                v.RadioGroup(
                                    v_model = None,
                                    style_= 'font-size: 0.5rem;',
                                    children=[
                                        v.Radio(label = 'Comma: ","'),
                                        v.Radio(label = 'Tab: " "'),
                                        v.Radio(label = 'Pipe: "|"')
                                    ]
                                )
                            ]
                        ),
                        v.Col(
                            children=[],
                        ),
                        v.Col(
                            children=[]
                        )
                    ]
                ),
                
            ]
        )

        self.uploaded_data = v.Container(
            children=[
                v.Card(children = [
                    "Upload Data"
                ])
            ]
        )
        super().__init__(
            class_=context_key,
            header_title=title,
            body_items=[
                self.data_upload,
                self.uploaded_data
            ],
            body_size={
                "width":"lg",
                "height":["340px", "100px"],
            },
            body_border_bottom = [True, True],
            body_background_color = ["rgb(255, 255, 255)", "rgb(248, 250, 252)"],
            align='center'
        )
class TabularEDAPImport(BaseCard):
    def __init__(self, app_context: object = None, context_key: str = "", title:str="", **kwargs):
        self.app_context = app_context
        self.context_key = context_key
        title = "EDAP에서 데이터 가져오기"

        self.edap_upload = v.Container(
            children = [
                v.Row(children = [
                    v.Col(children = [
                        v.Layout(children = [
                            v.Btn(color = 'primary', class_='ma-2 white--text', children = [
                                'EDAP 연결',
                                v.Icon(right=True, children=['mdi-cloud-upload']),
                            ]),
                        ]),
                    ]),
                ]),
            ]
        )

        self.uploaded_data = v.Container(
            children=[
                v.Card(children = [
                    "Upload Data"
                ])
            ]
        )
        # def _on_edap_upload(item, event = None, data = None):
        
        # self.edap_upload.on_event('click',_on_edap_upload)
        super().__init__(
            class_=context_key,
            header_title=title,
            body_items=[
                self.edap_upload,
                self.uploaded_data,
            ],
            body_size={
                "width":"1570px",
                "height":["340px", "100px"],
            },
            body_border_bottom = [True, True],
            body_background_color = ["rgb(255, 255, 255)", "rgb(248, 250, 252)"],
            align='center'
        )

class TabularPodImport(BaseCard):
    def __init__(self, app_context: object = None, context_key: str = "", title:str="", **kwargs):
        self.app_context = app_context
        self.context_key = context_key
        title = "POD"
        super().__init__(
            class_=context_key,
            header_title=title,
            body_items=[],
            body_size={
                "width":"1570px",
                "height":["340px", "100px"],
            },
            body_border_bottom = [True, True],
            body_background_color = ["rgb(255, 255, 255)", "rgb(248, 250, 252)"],
            align='center'
        )

    