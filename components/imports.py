import os
import ipyvuetify as v
from utils import get_or_create_class
from components.tab import BaseTab
from components.cards import BaseCard
from components.forms import DataSelect, DataSlider
from pathlib import Path
from IPython.core.display import HTML
from IPython.display import display, clear_output
from ipywidgets.widgets import widget_float
from ipywidgets.widgets.widget_layout import Layout
import pandas as pd
import io

from components.globals import html_UI_seperator
import ipywidgets as widgets
from components.cell import AppCell
from .upload.upload_widgets import EncodingWidgets, SeperatorWidgets, UploadWidgets,EDAPWidgets
#from .upload.uploadContext import AppContext

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

        ## Logging 기능
class TabularAIDUImport(BaseCard, AppCell):
    

    def __init__(self, app_context: object = None, context_key: str = "", title:str="", **kwargs):
        self.app_context = app_context
        self.context_key = context_key
        title = "AIDU에서 가져오기"
        from .upload.upload_utils import make_path_select_options

        
        
        # (1) 업로드 버튼 생성----------------------------------------------------------------
        self.button = v.Btn(color = 'primary', class_= 'ma-2 white--text', children = ['데이터 가져오기', v.Icon(right = True, children = ['mdi-cloud-upload'])])
        
        # (2) 데이터 경로 체크----------------------------------------------------------------
        # data_options = make_path_select_options(Path(os.sep,"..","..","..", "aihub","data"),recursive=True, extensions=None)
        data_dir = self.app_context.env_values["data_dir"]
        data_options = make_path_select_options(data_dir,recursive=True, extensions=None)
        workspace_data_options = make_path_select_options(os.getcwd(), recursive=False, extensions=['.csv','.tsv'])
       
        # (3) AIDU 업로드 데이터 선택----------------------------------------------------------
        data_list = []
        for i in range (0, len(data_options)):
            data_list.append(data_options[i][0])
        self.data_select = v.Select(v_model = None, label = '데이터',items = data_list, value = None,rows =7)
        def _data_change_select(widget, event = None, data = None):
            widget.value = widget.v_model
        self.data_select.on_event("change", _data_change_select)
        
        # (4) 작업 공간 데이터 선택-------------------------------------------------------------
        work_data_list = []
        for i in range(0, len(workspace_data_options)):
            work_data_list.append(workspace_data_options[i][0])
        self.workspace_data_select = v.Select(v_model = None, label = '작업공간 데이터',items = work_data_list,value=None,rows= 7)
        def _work_data_change_select(widget, event = None, data = None):
            widget.value = widget.v_model
        self.workspace_data_select.on_event("change",_work_data_change_select)

        # (5) 버튼 동작 및 필수 위젯, UI 구성------------------------------------------------------
        self.button.on_event('click', self.on_clicked)
        self.encoding_widgets = EncodingWidgets()
        self.upload_widgets = UploadWidgets()
        self.seperator_widgets = SeperatorWidgets()
        self.selected_datapath = None
        
        aidu_box = v.Container(children = [
            v.Html(
                tag = 'h5', 
                children = ["AIDU 플랫폼에 업로드한 데이터"]
            ),
            
            self.data_select
        ])
        workspace_box = v.Container(children = [
            v.Html(
                tag = 'h5',
                children = ["현재 경로에 생성한 데이터 (csv, tsv)"]
            ),
            self.workspace_data_select
        ])
        
        # 화면 그리기
        self.aidu_upload = v.Container(children = [
            v.Row(children = [
                v.Col(children = [aidu_box]),
                v.Col(children = [workspace_box])
                ]
                
            ),
            v.Row(children = [
                v.Col(children =[self.encoding_widgets()]),
                v.Col(children =[self.seperator_widgets()]),
                ]
                
            ),

            v.Row(style_ = 'padding-top:150px', children = [self.upload_widgets()]),
            v.Row(style_='padding-top:50px', children = [self.button])
            

        ])
        
        # (6) 데이터 개요 보여주기
        self.data_information = v.Container(
            style_ = "font-size:15x; font-weigth: bold; color = rgb(255,255,255)",
            children = [
                
            ]
        )


        super().__init__(
            app_context = self.app_context,
            class_=context_key,
            header_title_main=title,
            
            body_items=[
                
                self.aidu_upload,
                self.data_information

            ],
            body_size={
                "width": ["lg", "100px"],
                "height":["540px", "100px"],
            },
            body_border_bottom = [True, True],
            body_background_color = ["rgb(255, 255, 255)", "rgb(248, 250, 252)"],
            align='center'
        )

    # 버튼 핸들러-------------------------------------------------------------------------
    def on_clicked(self, widget, event = None, data = None):
        data_name = self.data_select.value.split('.')[0]
        data_dir = self.app_context.env_values["data_dir"]
        file_path = data_dir + self.data_select.value
        info = [True, ""]
        uploaded_data = self.upload_widgets.upload(data_name, info, self.encoding_widgets.encoding,sep = self.seperator_widgets.seperator, filepath = file_path)
        if uploaded_data is not None:
            self.app_context.tabular_workbook.create_new_work(data_name,uploaded_data) 
            self.upload_widgets.complete(data_name)
        self.data_shape = uploaded_data.shape
        buf = io.StringIO()
        uploaded_data.info(buf = buf)
        # self.data_info = buf.getvalue().split('\n')
        self.data_info = buf.getvalue()   
        self.data_select.value = None
        self.workspace_data_select.value = None
        self.button.disabled = False
        self.data_information.children = [self.data_info]
        
   

class TabularLocalImport(BaseCard, AppCell):
 

    def __init__(self, app_context: object = None, context_key: str = "", title:str="", **kwargs):
        self.app_context = app_context
        self.context_key = context_key
        title = "PC에서 업로드하기"
        
        # (1) 필수 위젯 및 UI 구성---------------------------------------------------------------
        self.matchedDataNames = []
        self.unmatchedDataNames = []
        self.upload_box = widgets.VBox()
        self.reset_uploader()
        self.encoding_widgets = EncodingWidgets()
        self.seperator_widgets = SeperatorWidgets()
        self.upload_widgets = UploadWidgets()
       
        self.local_upload = v.Container(
            children = [
                v.Row(children=[
                    v.Col(
                        children = [self.encoding_widgets()]
                    ),
                    v.Col(
                        children = [self.seperator_widgets()]
                    ),
                
                    ]
                ), 
                
                v.Divider(),
                v.Row(style_ = 'padding-top : 150px', children = [self.upload_widgets()]),
                
                v.Row(style_ = 'padding-top : 40px', children = [self.upload_box])
                
            ]
        )

        # (2) 데이터 업로드 경고 문구 추가
        self.data_information = v.Container(
            style_ = "font-size:15x; font-weigth: bold; color = rgb(255,255,255)",
            children = [
                
            ]
        )
        
        super().__init__(
            app_context = self.app_context,
            class_=context_key,            
            header_title_main=title,
            body_items=[
                self.local_upload,
                self.data_information
            ],
            body_size={
                "width":"lg",
                "height":["540px", "100px"],
            },
            body_border_bottom = [True, True],
            body_background_color = ["rgb(255, 255, 255)", "rgb(248, 250, 252)"],
            align='center'
        )
    
    # 업로드 핸들러------------------------------------------------------------------------------
    def _handle_uploaded(self, change):
         
            uploaded_dict = change["new"]
            file_name = list(uploaded_dict.keys())[0]
            data_name = os.path.splitext(file_name)[0]
            info = [True, ""]
            content = uploaded_dict[file_name]['content']
            uploaded_data = self.upload_widgets.upload(data_name, info, self.encoding_widgets.encoding, sep = self.seperator_widgets.seperator, content=content)
            if uploaded_data is not None:
                self.app_context.tabular_workbook.create_new_work(data_name, uploaded_data)
                self.upload_widgets.complete(data_name)
            self.data_shape = uploaded_data.shape
            buf = io.StringIO()
            uploaded_data.info(buf = buf)
            # self.data_info = buf.getvalue().split('\n')
            self.data_info = buf.getvalue() 
            self.data_information.children = [self.data_info]   

            self.reset_uploader()

    def reset_uploader(self):
        
        uploader = widgets.FileUpload(
            description = '데이터 업로드',
            accept='.csv,.csv_,.tsv',  # 확장자 제한 '.txt', '.pdf', 'image/*', 'image/*,.pdf'
            multiple=False,  # 복수 파일 업로드 불가
        )
                
        uploaderBtn = v.Tooltip(right=True, v_slots =[{
            'name': 'activator',
            'variable': 'tooltip',
            'children': v.Btn(v_on='tooltip.on', color = 'primary', class_='ma-2 white--text', children = [
               
                uploader
                ]),
            }], children=[
            'DRM 해제 문서만 업로드 가능'
        ]) 
        uploader.observe(self._handle_uploaded, names='value')
        self.upload_box.children = [uploaderBtn]

class TabularEDAPImport(BaseCard):
    def __init__(self, app_context: object = None, context_key: str = "", title:str="", **kwargs):
        self.app_context = app_context
        self.context_key = context_key
        title = "EDAP에서 데이터 가져오기"
        
        ##------------------##
        ## 테스트는 사내 망에서  ##
        ##------------------##

        # def on_clicked(self,btn):
        #     uploaded_data = self.edap_widgets.execute_query()
        #     data_name = self.edap_widgets.curr_table
        #     if uploaded_data is not None:
        #         # self.context.createJob(self.context.currPjtName, data_name)
        #         # self.context.addData(self.context.currJobID, data_name, uploaded_data)    
        #         # self.context.getCellOf('form-ctx-summary').redraw() 
        #         self.edap_widgets.append_bottom_right_box(widgets.HTML(f"<h5> {data_name} 데이터가 업로드되었습니다. </h5>"))
        
        # query_button = widgets.Button(description = "데이터 가져오기")
        # self.edap_widgets = EDAPWidgets(query_button)
        # query_button.on_click(self.on_clicked)
        # # with self.output:
        # #     display(self.edap_widgets())

        # self.edap_upload = v.Container(
        #     children = [self.edap_widgets()]
        # )


        # UI 배치용 더미 
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

        # self.uploaded_data = v.Container(
        #     children=[
        #         v.Card(children = [
        #             "Upload Data"
        #         ])
        #     ]
        # )
        # def _on_edap_upload(item, event = None, data = None):
        
        # self.edap_upload.on_event('click',_on_edap_upload)
        super().__init__(
            class_=context_key,
            header_title_main=title,
            body_items=[
                self.edap_upload,
                
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
        title = "가공데이터"
        super().__init__(
            class_=context_key,
            header_title_main=title,
            body_items=[],
            body_size={
                "width":"1570px",
                "height":["340px", "100px"],
            },
            body_border_bottom = [True, True],
            body_background_color = ["rgb(255, 255, 255)", "rgb(248, 250, 252)"],
            align='center'
        )

    