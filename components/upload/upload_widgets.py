from IPython.core.display import HTML
import ipywidgets as widgets
import ipyvuetify as v
import os
import re
from pathlib import Path
import pandas as pd
from IPython.display import display, clear_output
from ..upload.upload_utils import make_backtick_name
from impala.dbapi import connect

AIAN_EDAP_USER_ID="aidu"
AIAN_EDAP_USER_PW="new1234!"

sample_data ={
    'databases':
        ['aian','datastore','default','edu',
        'education', 'henry', 'it_ds_edu_team_1', 'kingsyda', 'kingsyda_work', 'ma_scy', 'ndap_temp', 'ods', 
        'pd_bdip', 'pd_bidw', 'pd_bigsight', 'pd_bizin', 'pd_bom', 'pd_cpsc', 'pd_cretop', 'pd_dss', 'pd_gfs', 
        'pd_idh', 'pd_inh', 'pd_isp', 'pd_ites', 'pd_kdapc_bas', 'pd_kdapc_cdr_dw', 'pd_kdapc_cdr_mart', 
        'pd_kdapc_cfc_dw', 'pd_kdapc_cfc_mart', 'pd_kdapc_imp', 'pd_kdapr_edw', 'pd_kdapr_ibada', 'pd_kos', 
        'pd_kpop_live_mart', 'pd_mars', 'pd_mbrain_dw', 'pd_mbrain_mart', 'pd_mbsp', 'pd_mdm', 'pd_mss', 
        'pd_prism', 'pd_publicdb', 'pd_wing', 'pj_ai_inv', 'pj_aih', 'pj_aiplay2020', 'pj_bdip', 'pj_lesson', 
        'pj_local_currency', 'pj_moin_trmn', 'pj_network', 'pj_network_1', 'pj_oneday_class', 'pj_packet', 
        'pj_python_training', 'pj_syda', 'pj_test_schema', 'pj_user', 'syda_data', 'syda_work', 'test_2022', 
        'test_category_db', 'test_db', 'tm_hb', 'workspace_group6'],          
    'tables':
        ['house_price','output10064107','output_10048717','output_10063058','output_10063506','output_10086456',
        'output_10126222','output_10138415','output_10143656','output_10143776','output_10148471','output_10149638',
        'output_10151984','output_10152046','output_10152083','output_82226130','output_bjp','output_khs','output_pyj',],
    'desc':
        [{'col_name': 'id', 'data_type': 'bigint', 'comment': ''},
         {'col_name': 'mssubclass', 'data_type': 'bigint', 'comment': ''},
         {'col_name': 'mszoning', 'data_type': 'string', 'comment': ''},
         {'col_name': 'lotfrontage', 'data_type': 'bigint', 'comment': ''},
         {'col_name': 'lotarea', 'data_type': 'bigint', 'comment': ''},
         {'col_name': 'street', 'data_type': 'string', 'comment': ''},
         {'col_name': 'saleprice', 'data_type': 'bigint', 'comment': ''}],
    'data':
        [{'id': 1, 'mssubclass': 60, 'mszoning': 'RL', 'lotfrontage': 65.0, 'lotarea': 8450, 'street': '포장', 'saleprice': 208500},
        {'id': 2, 'mssubclass': 20, 'mszoning': 'RL', 'lotfrontage': 80.0, 'lotarea': 9600, 'street': '포장', 'saleprice': 181500},
        {'id': 3, 'mssubclass': 60, 'mszoning': 'RL', 'lotfrontage': 68.0, 'lotarea': 11250, 'street': '포장', 'saleprice': 223500},
        {'id': 4, 'mssubclass': 70, 'mszoning': 'RL', 'lotfrontage': 60.0, 'lotarea': 9550, 'street': '포장', 'saleprice': 140000},
        {'id': 5, 'mssubclass': 60, 'mszoning': 'RL', 'lotfrontage': 84.0, 'lotarea': 14260, 'street': '포장', 'saleprice': 250000},
        {'id': 6, 'mssubclass': 50, 'mszoning': 'RL', 'lotfrontage': 85.0, 'lotarea': 14115, 'street': '포장', 'saleprice': 143000},
        {'id': 7, 'mssubclass': 20, 'mszoning': 'RL', 'lotfrontage': 75.0, 'lotarea': 10084, 'street': '포장', 'saleprice': 307000},
        {'id': 8, 'mssubclass': 60, 'mszoning': 'RL', 'lotfrontage': 65.0, 'lotarea': 8450, 'street': '포장', 'saleprice': 208500},
        {'id': 9, 'mssubclass': 20, 'mszoning': 'RL', 'lotfrontage': 80.0, 'lotarea': 9600, 'street': '포장', 'saleprice': 181500},
        {'id': 10, 'mssubclass': 60, 'mszoning': 'RL', 'lotfrontage': 68.0, 'lotarea': 11250, 'street': '포장', 'saleprice': 223500},
        {'id': 11, 'mssubclass': 70, 'mszoning': 'RL', 'lotfrontage': 60.0, 'lotarea': 9550, 'street': '포장', 'saleprice': 140000},
        {'id': 12, 'mssubclass': 60, 'mszoning': 'RL', 'lotfrontage': 84.0, 'lotarea': 14260, 'street': '포장', 'saleprice': 250000},
        {'id': 13, 'mssubclass': 50, 'mszoning': 'RL', 'lotfrontage': 85.0, 'lotarea': 14115, 'street': '포장', 'saleprice': 143000},
        {'id': 14, 'mssubclass': 20, 'mszoning': 'RL', 'lotfrontage': 75.0, 'lotarea': 10084, 'street': '포장', 'saleprice': 307000}]
}
class EncodingWidgets:
    def __init__(self):
        self.encoding = "UTF-8"
    def __call__(self):
        encoding_options = [
            ('UTF-8', 'UTF-8'),
            ('CP949 (한글)', 'CP949'),
            ('EUC-KR (한글)', 'EUC-KR')
        ]
        radio_buttons = v.RadioGroup(
            v_model = None,
            value = self.encoding,
            children=[
                v.Radio(label = encoding_options[0][0], value = encoding_options[0][1]),
                v.Radio(label = encoding_options[1][0], value = encoding_options[1][1]),
                v.Radio(label = encoding_options[2][0], value = encoding_options[2][1]),
            ]

        )
        def _change_radio(widget, event = None, data = None):
            widget.value = widget.v_model
            self.encoding = widget.value
           
        
        radio_buttons.on_event("change", _change_radio)
 
        return v.Col(
            style_ = 'max-height: 15px; font-size: 1rem; font-weight: bold; color: rgb(30, 41, 59);',
            children = [
                '데이터 인코딩 선택',
                radio_buttons,                         
                
            ]
        )
   
class SeperatorWidgets:
    def __init__(self):
        self.seperator = ","
    def __call__(self):
        seperator_options = [
            ("comma : \",\" ",","),
            ("tab : \"\t\"", "\t"),
            ("pipe : \"|\"","|"),
        ]

        radio_buttons = v.RadioGroup(
            v_model = None,
            disabled = False,
            value = self.seperator,
            mendatory = True,
            children = [
                v.Radio(label = seperator_options[0][0], value = seperator_options[0][1]),
                v.Radio(label = seperator_options[1][0], value = seperator_options[1][1]),
                v.Radio(label = seperator_options[2][0], value = seperator_options[2][1])
            ]
        )
        def _change_radio(widget, event = None, data = None):
            widget.value = widget.v_model
            self.seperator = widget.value


        radio_buttons.on_event("change", _change_radio)
        
        return v.Col(
            style_ = 'max-height: 15px; font-size: 1rem; font-weight: bold; color: rgb(30, 41, 59);',
            children = [
                '데이터 구분자 선택',
                radio_buttons
            ]
        ) 
  
class UploadWidgets:
    def __init__(self):
        self.box = v.Container(style_ = 'font-size: 1rem; font-weight: bold; color: rgb(0,0,0);', children = [""])
    def __call__(self):
        return self.box

    def upload(self, data_name, info, encoding, sep, filepath = None, content = None):
        from io import BytesIO
        widget_list = [v.Html(children = [info[1]])]
        widget_list.append(v.Html(
            tag = 'h5',
            cildren = ['대용량 파일 업로드는 오래 걸릴 수 있습니다'],
            ))
        widget_list.append(v.Html( 
            tag = 'h5',
            children = [f"{data_name} 데이터 업로드 중 입니다..."]
            ))
        self.box.children = widget_list
        uploaded_data = None
        if info[0]:
            encodings = ['UTF-8', 'CP949', 'EUC-KR']
            encodings.remove(encoding)
            encodings = [encoding] + encodings
            if filepath is not None and content is not None:
                self.box.children = [v.Html(
                    tag = 'h5',
                    children = [f"{data_name} : 파일경로가 잘못되었습니다."])]
            elif filepath is not None:
                filepath_or_buffer = filepath
            elif content is not None:
                filepath_or_buffer = BytesIO(content)
            else:
                filepath_or_buffer = None
                self.box.children = [v.Html(
                    tag = 'h5',
                    children = [f" {data_name} : 파일이 비어있습니다. "])]
            if filepath_or_buffer is not None:
                while (len(encodings) != 0 and uploaded_data is None):
                    encoding = encodings.pop(0)
                    uploaded_data = self.load_data(data_name, encoding=encoding, sep=sep, filepath=filepath, content=content)
            if uploaded_data is None:
                
                self.box.children = [v.Html(
                    tag = 'h5',
                    children = [f" {data_name} : 적합한 인코딩이 없습니다."])]                
        else:
            self.box.children = [v.Html(
                tag = 'h5',
                children = [f" {data_name} : 이미 업로드된 데이터입니다. "])]
        return uploaded_data


    def complete(self, data_name):
        self.box.children = [v.Html(
            tag = 'h5',
            children = [f" {data_name} 데이터가 업로드되었습니다. "])]

    def load_data(self, data_name, encoding, sep, filepath, content):
        from io import BytesIO
        uploaded_data = None
        try:
            if filepath is not None and content is not None:
                raise ValueError("filepath and content cannot assigned both")
            elif filepath is not None:
                filepath_or_buffer = filepath
            elif content is not None:
                filepath_or_buffer = BytesIO(content)
            else:
                # raise error
                filepath_or_buffer = None
            uploaded_data = pd.read_csv(filepath_or_buffer, sep=sep, encoding=encoding).replace({True: 1, False: 0})
            chk_col_all = re.compile('[^a-zA-Z0-9_]')
            column_list = uploaded_data.columns.tolist()
            for i in range(0, len(column_list)):
                if chk_col_all.search(column_list[i]) is not None:
                    raise Exception("데이터 컬럼명은 영문, 숫자, 그리고 '_'만 가능합니다. ")
            
            return uploaded_data
        except (UnicodeDecodeError, pd.errors.EmptyDataError) as e:
            pass
        except Exception as e:
            self.box.children = [
            v.Html(
                tag = 'h5',
                children = [
                    f"{data_name}.csv : 에러가 발생하였습니다. "]
                ),
            v.Html(
                tag = 'h5',
                children = [
                    f"에러 메시지 : {e} "]
                )
            ]
            raise               
       







class EDAPWidgets:
    def __init__(self, button):
        import os
        self.connect_status_html = v.Html()
        self.button = button
        from impala.dbapi import connect
        try:
            self.conn = connect(
                host="10.220.232.209",
                port=10000,
                auth_mechanism="LDAP",
                user=os.environ.get("AIAN_EDAP_USER_ID"),
                password=os.environ.get("AIAN_EDAP_USER_PW"),
                timeout = 100
                # user = "aidu",
                # password = "new1234!"
            )
        except Exception as e:
            self.conn = None
            self.connect_status_html.value = 'EDAP 연결이 올바르지 않습니다.' + str(e)

    def set_top_left_box(self):
        self.cursor.execute("""show databases""")
        databases = [dbName["database_name"] for dbName in self.cursor.fetchall()]
        # db_select = widgets.Select(
        #     options = databases,
        #     value = None,
        #     rows= 10
        #     )
        db_select = v.Select(
            v_model = None,
            items = databases,
            value = None,
            rows = 10
        )
        # db_select.observe(self.on_select_db, names = "value")
        self.top_left_box.children = [v.Html(
            tag = 'h5',
            children = ["EDAP 데이터베이스를 선택하세요"]),db_select]
    
    def set_top_right_box(self):
        self.cursor.execute("""show tables in """ + self.curr_db)
        tables = [tabName["tab_name"] for tabName in self.cursor.fetchall()]
        table_select = widgets.Select(
            options = tables,
            value = None,
            rows = 10
        )
        table_select = v.Select(
            v_model = None,
            items = tables,
            value = None,
            rows = 10
        )
        # table_select.observe(self.on_select_table, names = "value")
        self.top_right_box.children = [v.Html(
            tag = 'h5',
            children = [f"{self.curr_db}의 테이블을 선택하세요"]), table_select]
    
    def set_bottom_left_box(self):
        import pandas as pd
        db = make_backtick_name(self.curr_db)
        table = make_backtick_name(self.curr_table)
        info_output = widgets.Output()
        info_output.append_display_data(pd.read_sql("DESC " + db + "." + table, self.conn))
        self.bottom_left_box.children = [v.Html(
            tag = 'h5',
            children = [f" 테이블 {self.curr_table}의 정보입니다."]),info_output]
    
    def set_bottom_right_box(self):
        import re
        db = make_backtick_name(self.curr_db)
        table = make_backtick_name(self.curr_table)
        self.select_query = "SELECT * FROM " + db + "." + table + """ limit {limit}"""
        params = re.findall(r"\{([a-zA-Z0-9]*)\}", self.select_query)
        self.params = {p: "1000" for p in params}
        widget_list = [v.Html(
            tag = 'h5',
            children = [" 불러올 행의 수를 입력하세요. "])]
        for key,value in self.params.items():
            params_text = widgets.Text(value=value, placeholder=key)
            params_text.observe(self.on_param_change, names = "value")
            widget_list.append(widgets.HBox([v.Html(tag = 'h5', children = [f"{key}"]), params_text]))
        widget_list.append(self.button)
        self.bottom_right_box.children = widget_list
    def on_param_change(self, change):
        value = change["new"]
        if value.isnumeric():
            self.params[change["owner"].placeholder] = value if int(value)  < 1000000 else 1000000
    def append_bottom_right_box(self,widget):
            children = list(self.bottom_right_box.children)
            children.append(widget)
            self.bottom_right_box.children = children
    def execute_query(self):
        import pandas as pd
        try:
            data = pd.read_sql(self.select_query.format_map(self.params), self.conn)
        except Exception as e:
            self.append_bottom_right_box(v.Html(
                tag = 'h5',
                children = [f"데이터를 가져오는데 에러가 발생했습니다. {str(e)}"]))
            data = None
        return data

    def on_select_table(self,change):
        self.curr_table = change['new']
        self.set_bottom_left_box()
        self.set_bottom_right_box()

    def on_select_db(self,change):
        self.curr_db = change['new']
        self.set_top_right_box()

    def __call__(self):
        if self.conn is not None:
            self.top_left_box = widgets.VBox()
            self.top_right_box = widgets.VBox()
            self.bottom_left_box = widgets.VBox()
            self.bottom_right_box = widgets.VBox()
            top_layout = widgets.GridspecLayout(1,2)
            bottom_layout = widgets.GridspecLayout(1,2)
            top_layout[0,0] = self.top_left_box
            top_layout[0,1] = self.top_right_box
            bottom_layout[0,0] = self.bottom_left_box
            bottom_layout[0,1] = self.bottom_right_box

            widget = widgets.VBox([
                top_layout,
                bottom_layout
            ])
            self.cursor = self.conn.cursor(dictify = True)
            self.set_top_left_box()
            return widget
        else:
            return self.connect_status_html

class EdapDBMapper:
    '''
    edap 데이터베이스 연동
    aian_ide > aian > app > cells > cell_widgets > upload_widgets.py
    '''
    def __init__(
            self, 
            is_dev:bool=False,
            *args,
            **kwargs,
        ):
        self.is_dev=is_dev

        try:
            if self.is_dev:
                self.conn = None
            else:
                import os
                self.conn = connect(
                    host="10.220.232.209",
                    port=10000,
                    auth_mechanism="LDAP",
                    user=os.environ.get("AIAN_EDAP_USER_ID"),
                    password=os.environ.get("AIAN_EDAP_USER_PW"),
                )
                self.cursor = self.conn.cursor(dictify = True)

        except Exception as e:
            self.conn = None
            return e

    # aian_ide: set_top_left_box
    def fetch_db_names(self):
        if self.is_dev:
            return sample_data['databases'], str(len(sample_data['databases']))+ " databases fetched"

        try:
            self.cursor.execute("""show databases""")
            databases = [dbName["database_name"] for dbName in self.cursor.fetchall()]
            return databases, str(len(databases))+ " databases fetched"
        
        except Exception as e:
            return None, e
    
    # aian_ide: set_top_right_box
    def fetch_table_names(self, current_db):
        if self.is_dev:
            return sample_data['tables'], str(len(sample_data['tables']))+" tables fetched"
            
        try:
            self.cursor.execute("""show tables in """ + current_db)
            tables = [tabName["tab_name"] for tabName in self.cursor.fetchall()]
            return tables, str(len(tables))+" tables fetched"
        
        except Exception as e:
            return None, e
    
    # aian_ide: set_bottom_left_box
    def fetch_table_desc(self, current_db, current_table):
        if self.is_dev:
            return sample_data['desc'], current_db+" > "+current_table+" desc fetched" 
        try:
            import pandas as pd
            desc= pd.read_sql("DESC " + current_db + "." + current_table, self.conn)
            return desc.to_dict('records'), current_db+" > "+current_table+" desc fetched"
        
        except Exception as e:
            return None, e
    
    # aian_ide: set_bottom_right_box
    def fetch_rows(self, current_db, current_table, rows):
        if self.is_dev:
            return sample_data['data'], str(len(sample_data['data']))+"rows"
        try:
            import re
            import pandas as pd
            
            self.select_query = "SELECT * FROM " + current_db + "." + current_table + """ limit {limit}"""
            params = re.findall(r"\{([a-zA-Z0-9]*)\}", self.select_query)
            self.params = {p: rows for p in params}
            data = pd.read_sql(self.select_query.format_map(self.params), self.conn)                
                
            return data.to_dict('records'), str(len(data))+"rows"
        
        except Exception as e:
            return None, e
    
    # 커넥션 클로즈
    def __del__(self):
        if self.conn is not None:
            self.conn.close()
        return 'connection closed successfully'
'''
def test_edap_db_mapper():
    edap_mapper_op=EdapDBMapper(is_dev=False)
    edap_mapper_dev=EdapDBMapper(is_dev=True)
    
    assert edap_mapper_op.fetch_db_names() == edap_mapper_dev.fetch_db_names()
    assert edap_mapper_op.fetch_table_names(current_db='edu') == edap_mapper_dev.fetch_table_names(current_db='edu')
    assert edap_mapper_op.fetch_table_desc(current_db='edu', current_table='house_price') == edap_mapper_dev.fetch_table_desc(current_db='edu', current_table='house_price')
    assert edap_mapper_op.fetch_rows(current_db='edu', current_table='house_price', rows=7) == edap_mapper_dev.fetch_rows(current_db='edu', current_table='house_price', rows=7)
'''