import ipyvuetify as v
from components.buttons import StatedBtn
from components.cards import IconCard
from components.dialog import SimpleDialog


class TaskBaseView(v.Container):
    def __init__(self, app_context, context_key, title:str, workbook_card_data:list, **kwargs):
        self.app_context = app_context
        self.context_key = context_key
        self.title = title
        self.workbook_card_data = workbook_card_data

        # top_area: title + view option button
        self.title = v.Col(
            children = [self.title],
            style_ = "padding-left:40px; font-size:18px; font-weight:bold; color:#8f8f8f; \
                      display:flex; align-items:center;",
        )

        self.view_option_button = StatedBtn(
                state = 'icon',
                v_on='tooltip.on',
                icon = True,
                style_ = "",
                children = [v.Icon(children = "mdi-format-list-bulleted")],
            )

        self.view_option_tooltip = v.Tooltip(
                class_ = "",
                bottom=True, 
                v_slots=[{
                    'name': 'activator',
                    'variable': 'tooltip',
                    'children': [self.view_option_button],
                }],
                children = ['리스트로 보기'],
            )

        self.view_option_area = v.Col(
            class_= "",
            children = [self.view_option_tooltip],
            style_ = "display:flex; justify-content:flex-end; padding-right:40px;",
        )

        # dialog
        self.confrim_btn = v.Btn(
                children = ["확인"],
                small = True,
            )

        self.cancel_btn = v.Btn(
                children = ["취소"],
                small = True,
            )

        self.more_menu_dialog_contents = {
            'rename':{
                'title':'Workbook 이름 변경', 
                'body': v.TextField(
                    v_model = "",
                    style_ ="padding:10px 20px 0 20px;",
                )
            },
            'delete':{
                'title':'Workbook 삭제',
                'body': v.Col(
                    children = [],
                    style = ""
                ),
            },
        }
        self.more_menu_dialog = SimpleDialog(
            title = "",
            body = "",
            buttons = [ self.confrim_btn, self.cancel_btn ],
                size = {'width':'500px', 'height':'200px'},
                # style = {
                #     'card':"",
                #     "header":"",
                #     "body":"align-items:center; font-size:16px; color:#2f2f2f; padding:20px; \
                #         line-height:32px;",
                #     "footer":"padding-top:0; border-top:0; background-color:#ffffff;"
                # }
        )

        self.top_area = v.Row(
            style_ = 'margin:0; padding:0;',
            class_ = "",
            children = [self.title, self.view_option_area, self.more_menu_dialog],
        )

        # middle_area: workbook cards, dialog
        # workbook cards
        self.workbook_cards = [
            IconCard(
                workbook_type = card_data['workbook_type'],
                title = card_data['title'],
                text = card_data['text'],
                workbook_icon = card_data['workbook_icon'],
                workbook_color = card_data['workbook_color'],
                favorite = card_data['favorite'],
                size = {'width': '280px', 'height': '170px'},
                idx = idx,

            ) for idx, card_data in enumerate(self.workbook_card_data)
        ]   

        self.middle_area = v.Row(
            style_ = 'margin:0; padding:0; padding-left:40px; padding-right:25px; padding-top:20px;',
            class_ = "",
            children = self.workbook_cards
        )

        # bottom_area: 
        self.bottom_area = v.Row(
            style_ = 'margin:0; padding:0;',
            class_ = "",
        )

        super().__init__(
            class_ = "",
            style_="margin:0; padding:0;",
            children=[
                self.top_area,
                self.middle_area,
                self.bottom_area,
            ],
        )

        # callbacks: 모든 callback은 1차로 tasks.py 에서 처리
        self.controller = getattr(self.app_context, self.relavant_controller)

        # callbacks: (1) Workbook 열기
        self.last_clicked_card = None
        self.just_clicked_card = None
        def _on_click_workbook_card(item, event, data):
            self.app_context.ignore_progress_linear = True
            self.app_context.progress_overlay.start()
            
            self.idx = int(item.class_)
            self.just_clicked_card = self.workbook_cards[self.idx]
            self.just_clicked_card.class_list.add('now_in_use')

            if self.last_clicked_card:
                self.last_clicked_card.class_list.remove('now_in_use')

            # keep last clicked card
            self.last_clicked_card = self.just_clicked_card
                
            # call load_workbook function in controller 
            
            self.app_context.progress_overlay.update(50)
            if self.app_context.current_workbook:
                if self.just_clicked_card.title_text != self.app_context.current_workbook.current_workbook_name:
                    self.controller.load_workbook(self.just_clicked_card.workbook_type, self.just_clicked_card.title_text) # e.g. 'tabular', 'Untitled.ezx'
                else:
                    self.controller.return_to_current_workflow_stage()
            else:
                self.controller.load_workbook(self.just_clicked_card.workbook_type, self.just_clicked_card.title_text)
            self.app_context.progress_overlay.update(100)
            self.app_context.progress_overlay.stop()
            self.app_context.ignore_progress_linear = False

        for card in self.workbook_cards:
            card.children[0].children[0].on_event('click', _on_click_workbook_card)
            card.children[1].on_event('click', _on_click_workbook_card)

        # callbacks: (2) 이름 변경
        self.selected_workbook_name = ''
        def _on_select_rename(item, event, data):
            self.selected_workbook_name = item.class_.split('|')[-1].split('.')[0]
            self.more_menu_dialog_contents['rename']['body'].v_model = self.selected_workbook_name.split('.')[0]
            self.more_menu_dialog.update(self.more_menu_dialog_contents['rename'])
            self.more_menu_dialog.show()

            def _on_click_cancel_button(item, event, data):
                self.more_menu_dialog.value = 0

            def _on_click_confirm_button(item, event, data):
                self.controller.rename_workbook(
                    self.selected_workbook_name, 
                    self.more_menu_dialog.children[0].children[1].children[0].v_model, 
                    )            

            self.cancel_btn.on_event('click', _on_click_cancel_button)  
            self.confrim_btn.on_event('click', _on_click_confirm_button)

        # callbacks: (3) 삭제
        self.selected_workbook_full_name = ''
        def _on_select_delete(item, event, data):
            self.controller.check_active(self.selected_workbook_full_name)

            self.selected_workbook_full_name = item.class_.split('|')[-1]
            self.more_menu_dialog_contents['delete']['body'].children = [
                f"{self.selected_workbook_full_name} 파일을 삭제 하시겠습니까? 삭제된 파일은 복구할 수 없습니다."
                ]
            self.more_menu_dialog.update(self.more_menu_dialog_contents['delete'])
            self.more_menu_dialog.show()

            def _on_click_cancel_button(item, event, data):
                self.more_menu_dialog.value = 0

            def _on_click_confirm_button(item, event, data):
                self.controller.delete_workbook(self.selected_workbook_full_name)
                self.more_menu_dialog.value = 0
            
            self.cancel_btn.on_event('click', _on_click_cancel_button)  
            self.confrim_btn.on_event('click', _on_click_confirm_button)

        for workbook_card in self.workbook_cards:
            workbook_card.more_items.children[0].on_event('click', _on_select_rename)
            workbook_card.more_items.children[1].on_event('click', _on_select_delete)

    def show(self, target_area:object):
        self.target_area = target_area
        self.target_area.children = [self]

    def sort(self):
        pass

class TaskRecentView(TaskBaseView):
    def __init__(self, app_context, context_key, **kwargs):
        self.app_context = app_context
        self.context_key = context_key
        self.workbook_card_data = kwargs.get('workbook_card_data')
        self.relavant_controller = 'task_recent'

        super().__init__(
            self.app_context,
            self.context_key,
            title = '최근 작업 파일',
            workbook_card_data = self.workbook_card_data,
        )

class TaskFavoriteView(TaskBaseView):
    def __init__(self, app_context, context_key, **kwargs):
        self.app_context = app_context
        self.context_key = context_key
        self.workbook_card_data = kwargs.get('workbook_card_data')
        self.relavant_controller = 'task_favorite'

        super().__init__(
            self.app_context,
            self.context_key,
            title = '즐겨 찾기',
            workbook_card_data = self.workbook_card_data,
        )

class TaskAllView(TaskBaseView):
    def __init__(self, app_context, context_key, **kwargs):
        self.app_context = app_context
        self.context_key = context_key
        self.workbook_card_data = kwargs.get('workbook_card_data')
        self.relavant_controller = 'task_all'

        super().__init__(
            self.app_context,
            self.context_key,
            title = '전체 작업',
            workbook_card_data = self.workbook_card_data,
        )

