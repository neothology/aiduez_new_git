from numpy import size
import pandas as pd
import ipyvuetify as v
from utils import get_or_create_class

class TabularImportBaseView(v.Container):
    def __init__(
        self,
        app_context,
        context_key,
        left_area:list = [],
        right_area:list = [],
        middle_area:list = [],
        bottom_area:list = [],
        size:dict = {},
        style:dict = {},
        **kwargs
    ):
        self.app_context = app_context
        self.context_key = context_key

        self.style = {
            'left':"margin:0; padding-left:50px; padding-top:20px; height:250px;" + size.get('left', "") + style.get('left', ""),
            'right':"margin:0; padding:0; padding-top:20px; height:250px;" + size.get('right', "") + style.get('right', ""),
            'top':"margin:0; padding:0;" + size.get('top', "") + style.get('top', ""),
            'middle':"margin:0; padding:0; max-height:45px; margin-left:50px; margin-right:390px; border-bottom:1px solid #e0e0e0;\
                align-items:flex-end;" + size.get('middle', "") + style.get('middle', ""),
            'bottom':"margin:0; padding:0; height:100%;" + size.get('bottom', "") + style.get('bottom', ""),
            'all':"min-width:100%; min-height:100%; padding:0; display:flex; flex-direction:column;",
        }

        # work area left side - current data list in workbook
        self.work_area_contents_sub_area__left = v.Col(
            children = left_area,
            style_ = self.style['left'],
            class_ = f'{self.context_key}__work_area_contents_sub_area__left', # tabular_import_common_layout__work_area_contents_sub_area__left",
        )

        # work area right side - data list to be imported, etc
        self.work_area_contents_sub_area__right = v.Col(
            children = right_area,
            style_ = self.style['right'],
            class_ = f"{self.context_key}__work_area_contents_sub_area__right", # tabular_import_common_layout__work_area_contents_sub_area__right",
        )

        # merge left + right 
        self.work_area_contents_sub_area__top = v.Row(
            children = [
                self.work_area_contents_sub_area__left,
                self.work_area_contents_sub_area__right,
            ],
            style_ = self.style['top'],
            class_ = f"{self.context_key}__work_area_contents_sub_area__top", # tabular_import_common_layout__work_area_contents_sub_area__top",
        )

        # work area middle 
        self.work_area_contents_sub_area__middle = v.Row(
            children = middle_area,
            style_ = self.style['middle'],
            class_ = f"{self.context_key}__work_area_contents_sub_area__middle", # tabular_import_common_layout__work_area_contents_sub_area__middle",
        )        

        # work area bottom side - data info, etc.
        self.work_area_contents_sub_area__bottom = v.Row(
            children = bottom_area,
            style_ = self.style['top'],
            class_ = f"{self.context_key}__work_area_contents_sub_area__bottom", # tabular_import_common_layout__work_area_contents_sub_area__bottom",
        )         

        super().__init__(
            class_ = self.context_key,
            style_ = self.style['all'],
            children = [
                self.work_area_contents_sub_area__top,
                self.work_area_contents_sub_area__middle,
                self.work_area_contents_sub_area__bottom,
            ],
        )

    def show(self):
        self.target_area.children = [self]

class TabularImportPCView(TabularImportBaseView):
    def __init__(self, app_context, context_key, **kwargs):
        self.app_context = app_context
        self.context_key = context_key
        self.target_area = kwargs.get('target_area')
        self.workbook_data_list = kwargs.get('workbook_data_list')

        self.workbook_data_list_view = get_or_create_class(
            'select_table_card_no_header',
            self.app_context,
            context_key = 'tabular_data_import__workbook_data_list_view',
            title = 'Workbook 데이터 목록',
            data = self.workbook_data_list,
            size = {'width':'400px', 'height':'185px'},
            single_select = True,
        )

        self.select_encoding_options = get_or_create_class(
            'simple_radio_card',
            self.app_context,
            context_key = f'{self.context_key}__select_encoding_options',
            title = '인코딩 선택',
            direction = 'row',
            options = {
                'labels':['UTF-8', 'CP949(한글)', 'EUC-KR(한글)'],
                'values':['utf-8', 'cp949', 'euc-kr'],
            },
            size = {'width':'431px', 'height':'100px'},
            style_ = "font-size:14px;",
        )

        self.select_delimiter_options = get_or_create_class(
            'simple_radio_card',
            self.app_context,
            context_key = f'{self.context_key}__select_delimiter_options',
            title = '구분자 선택',
            direction = 'row',
            options = {
                'labels':['comma:","', 'tab:""', 'pipe:"|"'],
                'values':[',', '\t', '|'],
            },
            size = {'width':'431px', 'height':'100px'},
            style_ = "font-size:14px;",
        )

        select_import_options_area = v.Col(
            children = [
                self.select_encoding_options,
                v.Spacer(style_ = "min-height:20px"),
                self.select_delimiter_options,
            ],
            class_ = "",
            style_ = "padding:0;",
        )

        from ipyvuetify.extra import FileInput
        self.file_to_be_uploaded = None
        self.upload_file_textfield = FileInput(show_progress=False,multiple=False)

        self.file_upload_button = v.Btn(
                    style_ = "background-color:#636efa; color:white;",
                    children = ['가져오기'],
                    depressed = True,
                    disabled = True,
                )

        file_upload_button_row = v.Row(
            children = [self.file_upload_button],
            style_ = "width:95px; padding-left:30px; padding-bottom:29px;",
            class_ = "",
        )

        super().__init__(
            self.app_context,
            self.context_key,
            left_area = [self.workbook_data_list_view],
            right_area = [select_import_options_area],
            middle_area = [self.upload_file_textfield, file_upload_button_row],
            size = {
                'left':"max-width:40%;",
                'right':"max-width:60%;",
                'top':"max-height:250px;",
                'middle':"max-height:80px;",
            },
        )

        # event handlers : '가져오기' (비)활성화
        def _on_select_file(change):
            if self.upload_file_textfield.file_info == []:
                self.file_upload_button.disabled = True
            else:
                self.file_upload_button.disabled = False

        self.upload_file_textfield.observe(_on_select_file)

        # event handlers : click '가져오기'
        def _upload_file(item, event, data):
            self.upload_file_textfield.disabled = True
            self.file_upload_button.disabled = True
            encoding_option = self.select_encoding_options.selected_option
            delimiter_option = self.select_delimiter_options.selected_option
            controller = self.app_context.tabular_import_pc
            controller.load_data(self.upload_file_textfield, encoding_option, delimiter_option)
            
            self.upload_file_textfield.clear()
            self.upload_file_textfield.disabled = False
            
        self.file_upload_button.on_event('click', _upload_file)
    
    def update(self, data_name_list):
        self.workbook_data_list_view.update(data_name_list)

class TabularImportAIDUView(TabularImportBaseView):
    def __init__(self, app_context, context_key, **kwargs):
        self.app_context = app_context
        self.context_key = context_key
        self.target_area = kwargs.get('target_area')
        self.workbook_data_list = kwargs.get('workbook_data_list')
        self.aidu_data_list = kwargs.get('aidu_data_list')

        self.workbook_data_list_view = get_or_create_class(
            'select_table_card_no_header',
            self.app_context,
            context_key = 'tabular_data_import__workbook_data_list_view',
            title = 'Workbook 데이터 목록',
            data = self.workbook_data_list,
            size = {'width':'400px', 'height':'185px'},
            single_select = True,
        )

        self.aidu_data_list_view = get_or_create_class(
            'select_table_card_no_header',
            self.app_context,
            context_key = 'tabular_data_import__aidu_data_list_view',
            title = 'AIDU 데이터 목록',
            data = self.aidu_data_list,
            size = {'width':'400px', 'height':'185px'},
            select = True,
            single_select = True,
        )

        self.select_encoding_options = get_or_create_class(
            'simple_radio_card',
            self.app_context,
            context_key = f'{self.context_key}__select_encoding_options',
            title = '인코딩 선택',
            direction = 'row',
            options = {
                'labels':['UTF-8', 'CP949(한글)', 'EUC-KR(한글)'],
                'values':['utf-8', 'cp949', 'euc-kr'],
            },
            size = {'width':'400px', 'height':'100px'},
            style_ = "font-size:14px;",
        )

        self.select_delimiter_options = get_or_create_class(
            'simple_radio_card',
            self.app_context,
            context_key = f'{self.context_key}__select_delimiter_options',
            title = '구분자 선택',
            direction = 'row',
            options = {
                'labels':['comma:","', 'tab:""', 'pipe:"|"'],
                'values':[',', '\t', '|'],
            },
            size = {'width':'400px', 'height':'100px'},
            style_ = "font-size:14px;",
        )

        self.file_upload_button = v.Btn(
                    style_ = "background-color:#636efa; color:white;",
                    children = ['가져오기'],
                    depressed = True,
                )

        super().__init__(
            self.app_context,
            self.context_key,
            left_area = [
                self.workbook_data_list_view, 
                v.Spacer(style_ = "min-height:20px"),
                self.select_encoding_options],
            right_area = [
                self.aidu_data_list_view, 
                v.Spacer(style_ = "min-height:20px"),
                self.select_delimiter_options],
            middle_area = [self.file_upload_button],
            size = {
                'left':"max-width:40%; max-height:380px; min-height:380px;",
                'right':"max-width:60%; max-height:380px; min-height:380px;",
                'top':"max-height:250px; max-height:380px; min-height:380px;",
                'middle':"max-height:100px;",
            },
            style = {
                'left':"",
                'right':"",
                'top':"",
                'middle':"border:0; margin-right:405px; align-items:flex-start; justify-content:flex-end;",
            }
        )

        def _upload_file(item, event, data):
            if self.aidu_data_list_view.children[1].children[0].selected == []:
                raise Exception('선택된 AIDU 데이터가 없습니다.')

            self.file_upload_button.disabled = True
            encoding_option = self.select_encoding_options.selected_option
            delimiter_option = self.select_delimiter_options.selected_option
            controller = self.app_context.tabular_import_aidu
            controller.load_data(
                self.aidu_data_list_view.children[1].children[0].selected[0]['index'],
                encoding_option,
                delimiter_option,
            )          
            self.file_upload_button.disabled = False
        self.file_upload_button.on_event('click', _upload_file)

class TabularImportEDAPView(TabularImportBaseView):
    def __init__(self, app_context, context_key, **kwargs):
        from components.tables import EdapDataTable
        from components.upload.upload_widgets import EdapDBMapper
        from components.selector import SingleSelector
        from components.forms import SimpleInputCard

        self.app_context = app_context
        self.context_key = context_key
        self.target_area = kwargs.get('target_area')
        self.database_list = kwargs.get('workbook_data_list')
        self.table_list = kwargs.get('aidu_data_list')
        self.current_db= 'edu'
        self.current_table= 'house_price'
        
        edap_mapper=EdapDBMapper(is_dev=True)

        self.workbook_data_list_view = get_or_create_class(
            'select_table_card_no_header',
            self.app_context,
            context_key = 'tabular_data_import__workbook_data_list_view',
            title = '데이터베이스 목록',
            data=self.database_list,
            # size = {'width':'2500px', 'height':'185px'},
            select = True,
            single_select=True,
        )
        self.workbook_data_list_view.add_controls([v.Icon(children=['mdi-cached'],small=True)])

        self.df=pd.DataFrame({'NoData': [],})
        self.datatable = EdapDataTable(
            headers = [
                {'text': colname,'value': colname} for colname in self.df.columns.to_list()
            ],
            items = self.df.to_dict('records'),
            headline = "HEADLINE"
        )

        self.table_list_view = get_or_create_class(
            'select_table_card_no_header',
            self.app_context,
            context_key = 'tabular_data_import__aidu_data_list_view',
            title = '테이블 목록',
            data = self.table_list,
            size = {'width':'250px', 'height':'185px'},
            select = True,
            single_select=True,
        )
        self.table_list_view.add_controls([v.Icon(children=['mdi-cached'],small=True)])

        self.show_table_data = get_or_create_class(
            'simple_datatable_card',
            self.app_context,
            context_key = f'{self.context_key}__show_edap_data',
            title = '데이터 보기',
            datatable=self.datatable,
            size = {'width':'650px', 'height':'520px'},
            style_ = "font-size:14px;",
        )
        self.show_table_data.add_controls([v.Icon(children=['mdi-cached'],small=True)])

        self.select_row_range_options =get_or_create_class(
            'simple_input_card',
            self.app_context,
            context_key = f'{self.context_key}__input_row_range_options',
            title = '행 범위 입력',
            size = {'width':'250px', 'height':'100px'},
            style_ = "font-size:14px;",
        )

        self.file_upload_button = v.Btn(
            style_ = "background-color:#636efa; color:white;",
            children = ['가져오기'],
            depressed = True,
        )

        file_upload_button_row = v.Row(
            children = [self.file_upload_button],
            style_ = "width:600px; padding-left: 560px; padding-bottom:29px;",
            class_ = "",
        )

        super().__init__(
            self.app_context,
            self.context_key,
            left_area = [
                self.workbook_data_list_view,
                v.Spacer(style_ = "min-height:20px"),
                self.table_list_view,
                v.Spacer(style_ = "min-height:20px"),
                self.select_row_range_options,
            ],
            right_area = [
                self.show_table_data,
                v.Spacer(style_ = "min-height:25px"),
                file_upload_button_row
            ],
            middle_area = [
            ],
            size = {
                'left':"max-width:25%; max-height:380px; min-height:380px;",
                'right':"max-width:75%; max-height:380px; min-height:380px;",
                'top':"max-height:250px; max-height:380px; min-height:380px;",
                'middle':"max-height:100px;",
            },
            style = {
                'left':"",
                'right':"",
                'top':"",
                'middle':"border:0; margin-right:405px; align-items:flex-start; justify-content:flex-end;",
            }
        )
        def _show_db_list(item, event, data):
            self.workbook_data_list_view.update(
                data=pd.DataFrame(edap_mapper.fetch_db_names()[0]).rename(columns={0:'data_name'})
            )
        def _show_table_list(item, event, data):
            self.current_db=self.workbook_data_list_view.children[1].children[0].selected[0]['data_name']
            self.table_list_view.update(
                data=pd.DataFrame(edap_mapper.fetch_table_names(current_db=self.current_db)[0]).rename(columns={0:'data_name'})
            )
        def _show_data(item, event, data):
            self.current_table=self.table_list_view.children[1].children[0].selected[0]['data_name']
            current_row=self.select_row_range_options.body.children[0].children[0].v_model
            self.df=edap_mapper.fetch_rows(current_db=self.current_db, current_table=self.current_table, rows=current_row)[0]
            self.datatable = EdapDataTable(
                headers = [
                    {'text': colname,'value': colname} for colname in self.df[0].keys()
                ],
                items = self.df,
                headline = "HEADLINE"
            )
            self.show_table_data.body.children[0].children=[self.datatable]
        def _upload_file(item, event, data):
            controller = self.app_context.tabular_import_edap
            controller.load_data(
                data_name=self.current_table,
                data=pd.DataFrame(self.df),
            ) 
        self.workbook_data_list_view.header.children[1].children[0].on_event('click',_show_db_list)
        self.table_list_view.header.children[1].children[0].on_event('click',_show_table_list)
        self.show_table_data.header.children[1].children[0].on_event('click',_show_data)
        self.file_upload_button.on_event('click',_upload_file)
        