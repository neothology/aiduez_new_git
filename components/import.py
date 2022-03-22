import os
import ipyvuetify as v
from utils import get_or_create_class
from components.tab import BaseTab
from components.cards import BaseCard
from components.dialog import BaseDialog
from pathlib import Path
from IPython.core.display import HTML
from IPython.display import display, clear_output
from ipywidgets.widgets import widget_float
from ipywidgets.widgets.widget_layout import Layout
import pandas as pd


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
class TabularAIDUImport(BaseCard, AppCell):
    

    def __init__(self, app_context: object = None, context_key: str = "", title:str="", **kwargs):
        self.app_context = app_context
        self.context_key = context_key
        title = "AIDU에서 가져오기"
        from .upload.upload_utils import make_path_select_options

        
        

        self.button = v.Btn(color = 'primary', class_= 'ma-2 white--text', children = ['데이터 가져오기', v.Icon(right = True, children = ['mdi-cloud-upload'])])
        data_options = make_path_select_options(Path(os.sep, "aihub","data"),recursive=True, extensions=None)
        # data_options = make_path_select_options(Path(os.sep, "opt","code","aiduez","data"),recursive=True, extensions=None)
        # data_options = os.listdir('data')
        workspace_data_options = make_path_select_options(os.getcwd(), recursive=False, extensions=['.csv','.tsv'])
        # self.data_select = widgets.Select(options = data_options, value = None,rows =7)
        data_list = []
        for i in range (0, len(data_options)):
            data_list.append(data_options[i][0])
        self.data_select = v.Select(label = 'Data',items = data_list, value = None,rows =7)
        # self.workspace_data_select = widgets.Select(options = workspace_data_options,value=None,rows= 7)
        self.workspace_data_select = v.Select(items = [workspace_data_options],value=None,rows= 7)
        self.data_select.observe(self.on_data_select,names="value")
        self.workspace_data_select.observe(self.on_data_select, names="value")
        self.button.on_event('click', self.on_clicked)
        self.encoding_widgets = EncodingWidgets()
        self.upload_widgets = UploadWidgets()
        self.seperator_widgets = SeperatorWidgets()
        self.selected_datapath =None
        aidu_box = v.Card(children = [
            v.Html(
                tag = 'h5', 
                children = ["AIDU 플랫폼에 업로드한 데이터"]
            ),
            
            self.data_select
        ])
        # workspace_box = widgets.VBox([widgets.HTML("<h5> 현재 경로에 생성한 데이터 (csv, tsv) </h5>"), self.workspace_data_select])
        workspace_box = v.Container(children = [
            v.Html(
                tag = 'h5',
                children = ["현재 경로에 생성한 데이터 (csv, tsv)"]
            ),
            self.workspace_data_select
        ])
        # with self.output:
        #     display(widgets.VBox([widgets.HBox([aidu_box, workspace_box]), widgets.HTML(html_UI_seperator), widgets.HBox([self.encoding_widgets(), self.seperator_widgets()]), widgets.HTML(html_UI_seperator), self.upload_widgets(), self.button ]))

        self.aidu_upload = v.Container(children = [
            v.Row(children = [
                v.Col(children = [aidu_box]),
                v.Col(children = [workspace_box])
                ]
                
            ),
            v.Row(children = [
                v.Col(children =[self.encoding_widgets()]),
                v.Col(children =[self.seperator_widgets()])
                ]
                
            ),

            v.Row(style_ = 'padding-top:150px', children = [self.upload_widgets()]),
            v.Row(style_='padding-top:50px', children = [self.button])
            

        ])



   
        
        super().__init__(
            class_=context_key,
            header_title=title,
            
            body_items=[
                
                self.aidu_upload

            ],
            body_size={
                "width": ["lg", "100px"],
                "height":["540px", "100px"],
            },
            body_border_bottom = [True, True],
            body_background_color = ["rgb(255, 255, 255)", "rgb(248, 250, 252)"],
            align='center'
        )
    def on_data_select(self, change):
            self.button.disabled = False
            self.selected_datapath = change["new"]
    

    def on_clicked(self,widget, event, data):
        data_name = os.path.splitext(self.selected_datapath.name)[0]
        info = self.app_context.validatePipe(data_name, 'add_data')
        uploaded_data = self.upload_widgets.upload(data_name, info, self.encoding_widgets.encoding,sep = self.seperator_widgets.seperator, filepath = self.selected_datapath)
        if uploaded_data is not None:
            # self.context.createJob(self.context.currPjtName, data_name)
            # self.context.addData(self.context.currJobID, data_name, uploaded_data)    
            # self.context.getCellOf('form-ctx-summary').redraw()
            self.app_context.addData(data_name,uploaded_data) 
            self.upload_widgets.complete(data_name)        
        self.data_select.value = None
        self.workspace_data_select.value = None
        self.button.disabled = True

class TabularLocalImport(BaseCard, AppCell):
 

    def __init__(self, app_context: object = None, context_key: str = "", title:str="", **kwargs):
        self.app_context = app_context
        self.context_key = context_key
        title = "PC에서 업로드하기"
        
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
        
        super().__init__(
            class_=context_key,
            header_title=title,
            body_items=[
                # self.data_upload,
                # self.uploaded_data
                self.local_upload
            ],
            body_size={
                "width":"lg",
                "height":["340px", "100px"],
            },
            body_border_bottom = [True, True],
            body_background_color = ["rgb(255, 255, 255)", "rgb(248, 250, 252)"],
            align='center'
        )
    def _handle_uploaded(self, change):
            
            uploaded_dict = change["new"]
            file_name = list(uploaded_dict.keys())[0]
            data_name = os.path.splitext(file_name)[0]
            info = self.app_context.validatePipe(data_name, 'add_data')
            content = uploaded_dict[file_name]['content']
            uploaded_data = self.upload_widgets.upload(data_name, info, self.encoding_widgets.encoding, sep = self.seperator_widgets.seperator, content=content)
            if uploaded_data is not None:
                # Pipline 작업 할 것
                # self.app_context.createJob(self.app_context.currPjtName, data_name)
                # self.app_context.addData(self.context.currJobID, data_name, uploaded_data)
                # self.app_context.getCellOf('form-ctx-summary').redraw()
                self.app_context.addData(data_name, uploaded_data)
                self.upload_widgets.complete(data_name)
              

            self.reset_uploader()


    def reset_uploader(self):
        
        uploader = widgets.FileUpload(
            description = '데이터 업로드',
            accept='.csv,.csv_,.tsv',  # Accepted file extension e.g. '.txt', '.pdf', 'image/*', 'image/*,.pdf'
            multiple=False,  # True to accept multiple files upload else False
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
        # def on_clicked(self,btn):
        #     uploaded_data = self.edap_widgets.execute_query()
        #     data_name = self.edap_widgets.curr_table
        #     if uploaded_data is not None:
        #         self.context.createJob(self.context.currPjtName, data_name)
        #         self.context.addData(self.context.currJobID, data_name, uploaded_data)    
        #         self.context.getCellOf('form-ctx-summary').redraw() 
        #         self.edap_widgets.append_bottom_right_box(widgets.HTML(f"<h5> {data_name} 데이터가 업로드되었습니다. </h5>"))
        
        # query_button = widgets.Button(description = "데이터 가져오기")
        # self.edap_widgets = EDAPWidgets(query_button)
        # query_button.on_click(self.on_clicked)
        # # with self.output:
        # #     display(self.edap_widgets())

        # self.edap_upload = v.Container(
        #     children = [self.edap_widgets()]
        # )

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
            header_title=title,
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

    