import ipyvuetify as v
from components.buttons import StatedBtn
from components.cards import IconCard


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

        self.top_area = v.Row(
            style_ = 'margin:0; padding:0;',
            class_ = "",
            children = [self.title, self.view_option_area]
        )

        # middle_area: workbook cards
        # workbook cards
        self.workbook_cards = [
            IconCard(
                workbook_type = card_data['workbook_type'],
                title = card_data['title'],
                text = card_data['text'],
                workbook_icon = card_data['workbook_icon'],
                workbook_color = card_data['workbook_color'],
                favorite = card_data['favorite'],
                size = {'width': '280px', 'height': '200px'},

            ) for card_data in self.workbook_card_data
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

        # callbacks:
        ##  click on workbook card
        def _on_click_workbook_card(item, event, data):
            self.selected = item

        for workbook_card in self.workbook_cards:
            workbook_card.on_event('click', _on_click_workbook_card)

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

        super().__init__(
            self.app_context,
            self.context_key,
            title = '전체 작업',
            workbook_card_data = self.workbook_card_data,
        )

