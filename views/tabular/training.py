from typing import Dict
import ipyvuetify as v
import logging
from ludwig.api import LudwigModel
import ipywidgets as widgets
from IPython.display import display
import shutil
import os   
import json
import numpy as np
from components.cards import BaseCard
from components.forms import DataSelect, DataSlider, LabeledSelect, SimpleSlider
from components.buttons import StatedBtn
from components.layouts import IndexRow
from components.cards import SmallHeaderCard
from components.dialog import BaseDialog
from utils import delete_files_in_dir

class TabularModel:
    def __init__(
        self, 
        app_context: object = None,
        context_key: str = None,
        **kwargs
        ):

        self.app_context = app_context
        self.context_key = context_key
        self.current_exp_and_model_name = ''

    def train(self, output_logs, output_plots, **kwargs):
        self.app_context.progress_linear.active = True
        config = self.app_context.tabular_ai_training__training_options.retrieve_config()
        self.output_logs = output_logs
        self.output_plots = output_plots
        self.current_model = LudwigModel(config, logging_level = logging.INFO)
        self.data_name = self.app_context.tabular_dataset.current_data_name
        self.current_model_name = 'latest'
        self.current_exp_and_model_name = f'{self.data_name}_{self.current_model_name}'
        self.dataset = self.app_context.tabular_dataset.current_data
        self.output_directory =  self.app_context.current_workbook.current_models_dir # e.g. /aihub/workspace/tmp/workbook/works/titanic_train/models

        # 모델 결과 Dialog 에 모델명 추가
        self.app_context.tabular_ai_training__train_result.children[0].title_sub.children = [f'모델명: {self.current_exp_and_model_name}']
        
        # clear output directory if model_name is 'latest'
        if self.current_model_name == 'latest':
            delete_files_in_dir(self.output_directory)

        with self.output_logs:
            self.eval_stats, self.train_stats, self.preprocessed_data, self.output_dir = self.current_model.experiment(
                dataset = self.dataset,
                experiment_name = self.data_name, 
                model_name = self.current_model_name,
                output_directory = self.output_directory,
                skip_save_processed_input = True,
                skip_save_logs = True,
            )
            display(widgets.HTML("<br><br>"))

        self.metadata = self.current_model.training_set_metadata # dict

        self.output_plots.children = [self.app_context.tabular_ai_training__train_result.make_plots(
            self.train_stats, # train_statistics.json
            self.eval_stats, # test_statistics.json
            self.metadata, # model/training_set_metadata.json
        )]

        # save output_logs
        # e.g. /aihub/workspace/tmp/workbook/works/titanic_train/models/titanic_train_latest
        self.current_train_result_dir = f'{self.output_directory}/{self.data_name}_{self.current_model_name}'
        ludwig_log_file = '/aihub/workspace/tmp/ludwig.log'
        result_logs_file =  os.path.join(self.current_train_result_dir, 'result_logs.txt')
        shutil.move(ludwig_log_file, result_logs_file) 

        # save training config
        self.app_context.tabular_ai_training__training_options.save_config(self.current_train_result_dir)

        # save training options
        self.work_state_dir = self.app_context.current_workbook.current_work_state_dir

        # set model in model_save_dialog text_field
        self.app_context.tabular_ai_training__train_result.children[0].model_save_body.v_model = self.current_model_name
        self.app_context.tabular_ai_training__train_result.children[0].model_save_body.prefix = f'{self.data_name}_'

        # acivate buttons in train_result_dialog
        self.app_context.tabular_ai_training__train_result.children[0].save_button.disabled = False
        self.app_context.tabular_ai_training__train_result.children[0].more_button.disabled = False
        self.app_context.tabular_ai_training__train_result.children[0].close_button.disabled = False

        # update workbook profile
        self.app_context.current_workbook.save_workbook(model = self.current_model_name)

        # save workbook
        self.app_context.current_workbook.save_workbook()

        self.app_context.progress_linear.active = False

    def save_as(self, exp_name, model_name: str):
        # update: current_model_name, current_exp_and_model_name, current_train_result_dir
        self.current_model_name = model_name
        self.current_exp_and_model_name = f'{self.data_name}_{self.current_model_name}'
        from_dir = self.current_train_result_dir
        to_dir = f'{self.output_directory}/{self.current_exp_and_model_name}'
        if from_dir == to_dir:
            raise Exception('from_dir and to_dir are same')
        shutil.copytree(from_dir, to_dir)
        self.current_train_result_dir = to_dir

    def load_model(self, model_name: str):
        pass

class TabularModelContext(v.Row):
    def __init__(self, app_context:object = None, context_key:str = '', **kwargs):
        self.app_context = app_context
        self.context_key = context_key

        self.workbook = self.app_context.current_workbook
        self.dataset = self.app_context.tabular_dataset

        self.data_name_list = self.dataset.data_name_list
        self.current_data_name = self.dataset.current_data_name

        self.style = {
            'row': 'width:1570px; align-self:center;',
            'data_selector': 'max-width:400px;',
        }

        self.data_selector = v.Select(
            v_model = self.current_data_name,
            items = self.data_name_list,
            attach = True,
            dense = True,
            filled = True,
            label = '데이터',
            class_ = "tabula-data-selector",
            style_ = self.style['data_selector'],
        )

        def _on_data_selector_change(item, event=None, data=None):
            self.workbook.change_work(item.v_model)

        self.data_selector.on_event('change', _on_data_selector_change)        

        super().__init__(
            style_ = self.style['row'],
            children = [self.data_selector],
        )

class TabularTrainActivator(v.Col):
    def __init__(
        self,
        app_context:object = None,
        context_key:str = None,
        title:str = "",
        **kwargs,
    ):
        self.app_context = app_context
        self.style = {
            'row': 'display:flex; flex-direction:row; padding:0; padding-top:12px; width:50%; justify-content:flex-end;',
            'text': 'padding-right:15px; padding-top:10px;',
            'button_result': 'width:100px; height:36px; margin-right:5px; background-color:#388e3c; color:white;',
            'button_train': 'width:100px; height:35px; background-color:#636efa; color:white;',
            } 

        self.target_yn = v.Html(
            tag = 'h4',
            children = ['출력 데이터가 없습니다'],
            attributes = {
                'style': self.style['text'],
            },
        )

        self.train_activator = v.Btn(
            style_ = self.style['button_train'],
            children = ['학습하기'],
            rounded = True,
            disabled = True,
        )

        self.show_result_btn = v.Btn(
            style_ = self.style['button_result'],
            children = ['결과 보기'],
            rounded = True,
        )
        self.show_result_btn.hide()

        super().__init__(
            children = [ self.target_yn, self.show_result_btn, self.train_activator],
            style_ = self.style['row'],
        )

        def _activate_model_train(item, event=None, data=None):

            self.train_result = self.app_context.tabular_ai_training__train_result
            self.train_result.button_chart_view.hide()
            self.train_result.button_chart_view.disabled = True

            self.train_result.clear_contents()
            self.train_result.children[0].children[1].children = [self.train_result.output_logs]

            self.train_result.show()
            
            self.model = self.app_context.tabular_model
            self.model.train(
                output_logs = self.train_result.output_logs,
                output_plots = self.train_result.output_plots,
            )
            self.train_result.button_chart_view.disabled = False
            self.train_result.button_chart_view.show()

            self.show_result_btn.show()

        def _show_train_result(item, event=None, data=None):
            
            self.app_context.tabular_ai_training__train_result.children[0].save_button.disabled = False
            self.app_context.tabular_ai_training__train_result.children[0].more_button.disabled = False
            self.app_context.tabular_ai_training__train_result.children[0].close_button.disabled = False
            
            self.train_result.show()

        self.train_activator.on_event('click', _activate_model_train)
        self.show_result_btn.on_event('click', _show_train_result)


class TabularTrainResult(BaseDialog):

    def __init__(
        self, 
        app_context:object = None,
        context_key:str = "",
        title:str = "",
        **kwargs,
        ):
        self.app_context = app_context
        self.style = {}

        # result ouput for training result
        self.output_logs = widgets.Output(
        )   
        self.output_plots = v.Container(
            children = [""],
        )

        body_items = [self.output_logs]

        # select options
        self.button_text_view = v.Btn(
                    small = True,
                    plain = True,
                    depressed = True,
                    text = True,
                    disabled = True,
                    children = ['텍스트 로그'],
                    style_ = 'color:rgb(0,0,0, 0.87) !important;',
                )

        self.button_chart_view = v.Btn(
                    small = True,
                    plain = True,
                    depressed = True,
                    text = True,
                    disabled = True,
                    children = ['차트 보기'],
                    style_ = 'color:rgb(0,0,0, 0.87) !important;',
                )
        self.button_chart_view.hide()

        def _on_click_button_chart_view(item, event=None, data=None):
            self.children[0].children[2].children = [self.output_plots]
            self.button_chart_view.disabled = True
            self.button_text_view.disabled = False

        def _on_click_button_text_view(item, event=None, data=None):
            self.children[0].children[2].children = [self.output_logs]
            self.button_text_view.disabled = True
            self.button_chart_view.disabled = False

        self.button_chart_view.on_event('click', _on_click_button_chart_view)
        self.button_text_view.on_event('click', _on_click_button_text_view)

        self.output_selector = v.Row(
            style_ = "margin: 0px; width:100%; max-height:33px; padding:0 12px; background-color:#f1f1f1; border-top:1px solid #e0e0e0;",
            children = [self.button_text_view, self.button_chart_view],
        )

        super().__init__(
            v_slots = [{
                # 'name': 'activator',
                # 'variable': 'x',
                # 'children': train_button,
                }],
            header_title_main = '학습 결과',
            header_title_sub = '모델명: ',
            header_bottom = self.output_selector,
            body_items = body_items,
            body_size = {'width': '90vw', 'height': ['80vh']},
            body_border_bottom = [True],
            body_background_color = ["rgb(255, 255, 255)"],
            align = 'center',
            more = True,
            close = True,
            save = True,
            class_ = context_key,
            app_context = self.app_context,
        )    

        # make call-back function for saving


        # self.save_button.on_event(
        #     'click', 
        #     self.app_context.tabular_model.save_as('model_name'),
        #     )

    def clear_contents(self):
        self.output_logs.clear_output()
        self.output_plots.children = [""]

    def show(self):
        self.value = 1
        self.value = 2

    def close(self):
        self.value = 0

    def make_plots(self, train_stats, eval_stats, meta_data):

        def make_f1_score_plot(str2idx, str2freq, idx2str, per_class_stats):
            import plotly.graph_objects as go
            import plotly
            from plotly.subplots import make_subplots
            subplots = make_subplots(rows=1, cols=2, specs=[[{"secondary_y": True}, {"secondary_y": True}]], subplot_titles=[
                                    "f1 score & frequency sorted by f1 score", "f1 score & frequency sorted by frequency"])
            k=10
            idx2freq = {str2idx[key]: val for key, val in str2freq.items()}
            str2f1 = {label_f1:class_stats_dict['f1_score'] for label_f1,class_stats_dict in per_class_stats.items()}
            idx2str=idx2str[::-1]
            idx2f1 = [str2f1[label] for label in idx2str[:k]]

            freq_sorted_by_freq = np.array(list(sorted(idx2freq,reverse=True))[:k], dtype=np.int32)
            f1_sorted_by_freq = np.nan_to_num(np.array(idx2f1, dtype=np.float32))
            label_sorted_by_freq = np.array(idx2str[:k])


            str2f1_sorted_by_f1 = dict(sorted(str2f1.items(), key=lambda item:item[1],reverse=True))
            str2freq = {key:str2freq[key] for key in str2f1_sorted_by_f1.keys()}
            f1_sorted_by_f1 =  np.nan_to_num(np.array(list(str2f1_sorted_by_f1.values())[:k],dtype=np.float32))
            freq_sorted_by_f1 = np.array(list(str2freq.values())[:k],dtype=np.int32)
            label_sorted_by_f1 = np.array(list(str2f1_sorted_by_f1.keys())[:k])

            colors = plotly.colors.DEFAULT_PLOTLY_COLORS
            subplots.add_trace(go.Scatter(x=label_sorted_by_f1, y=f1_sorted_by_f1,
                                        name="f1 score", line_color=colors[0], legendgroup=0), row=1, col=1)
            subplots.add_trace(go.Scatter(x=label_sorted_by_f1, y=freq_sorted_by_f1, name="frequency",
                                        line_color=colors[1], legendgroup=1), row=1, col=1, secondary_y=True)
            subplots.add_trace(go.Scatter(x=label_sorted_by_freq, y=freq_sorted_by_freq, name="frequency",
                                        line_color=colors[1], showlegend=False, legendgroup=1), row=1, col=2)
            subplots.add_trace(go.Scatter(x=label_sorted_by_freq, y=f1_sorted_by_freq, name="f1 score",
                                        line_color=colors[0], showlegend=False, legendgroup=0), row=1, col=2, secondary_y=True)

            subplots.update_xaxes(type='category',tickangle =-45,row=1, col=1)
            subplots.update_xaxes(type='category',tickangle =-45,row=1, col=2)
            subplots.update_xaxes(type='category',row=1, col=2)
            subplots.update_yaxes(title_text="f1 score", row=1, col=1)
            subplots.update_yaxes(title_text="frequency", row=1,
                                col=1, secondary_y=True)
            subplots.update_yaxes(title_text="frequency", row=1, col=2)
            subplots.update_yaxes(title_text="f1 score", row=1,
                                col=2, secondary_y=True)

            return go.FigureWidget(subplots)

        def make_confusion_matrix_plot(confusion_matrix, feature_name, idx2str, per_class_stats):
            import plotly.graph_objects as go
            import plotly.figure_factory as ff
            import plotly.express as px
            import ipywidgets as widgets
            from scipy.stats import entropy
            top_n_classes = min(10, len(confusion_matrix))
            confusion_matrix = np.array(confusion_matrix)
            confusion_matrix = confusion_matrix[:top_n_classes, :top_n_classes]
            labels = idx2str[:top_n_classes]
            metrics = np.array([[per_class_stats[label]["recall"], per_class_stats[label]
                                ["precision"], per_class_stats[label]["f1_score"]] for label in labels])
            cm_labels = list(
                map(lambda label: feature_name + ': ' + str(label), labels))
            custom_data = np.stack([np.diag(metrics[:, index])
                                    for index in range(metrics.shape[1])], axis=-1)
            heatmap = ff.create_annotated_heatmap(z=confusion_matrix, annotation_text=confusion_matrix, x=cm_labels, y=cm_labels, customdata=custom_data,
                                                hovertemplate="재현율: %{customdata[0]:.4f} <br>정밀도: %{customdata[1]:.4f} <br>F1 score: %{customdata[2]:.4f} <extra></extra>", colorscale="Viridis", showscale=True)
            heatmap.update_layout(title={"text": f"Confusion Matrix of {feature_name}"}, xaxis={"title": "Predicted value",
                                                                                                "tickangle": -45, "type": "category"}, yaxis={"title": "Actual value", "type": "category", "autorange": "reversed"})
            entropies = [round(entropy(row), 4) if np.count_nonzero(
                row) > 0 else 0 for row in confusion_matrix]
            np_entropies = np.array(entropies)
            asc_index = np.argsort(np_entropies)
            asc_entropies = np_entropies[asc_index]
            asc_labels = [labels[i] for i in asc_index]
            entropy_barplot = px.bar(x=asc_entropies, y=asc_labels)
            entropy_barplot.update_layout(title={"text": f"classes ranked by entropy of {feature_name} confusion Matrix row"}, xaxis={
                                        "title": "Entropy by confusion matrix row : -sum(Pk*log(pk))"}, yaxis={"title": "classes", "type": "category"})
            return widgets.HBox([go.FigureWidget(heatmap), go.FigureWidget(entropy_barplot)])

        def make_roc_curve(roc_curve, feature_name):
            fpr = roc_curve["false_positive_rate"]
            tpr = roc_curve["true_positive_rate"]
            import plotly.graph_objects as go
            fig = go.Figure()
            fig.add_trace(go.Scatter(x=fpr, y=tpr, name="model classifier"))
            fig.add_trace(go.Scatter(x=[0, 1], y=[0, 1], mode="lines", name="random classifier", line={
                        "dash": "dash", "color": "black"}))
            fig.update_layout(title={"text": f"ROC curve of {feature_name}"}, xaxis={
                            "title": "False positive rate"}, yaxis={"title": "True positive rate"})
            fig.update_traces(
                hovertemplate="True positive rate: %{y}<br> False positive rate: %{x}<extra></extra>"
            )
            fig.update_xaxes(
                range=[0, 1],
                constrain="domain"
            )
            fig.update_yaxes(
                scaleanchor="x",
                scaleratio=1,
            )

            return go.FigureWidget(fig)

        def make_eval_stats_plot_dict(eval_stats, meta_data) -> dict:
            # initialize
            eval_stats_plot_dict = {}
            for feature_name, stats_dict in eval_stats.items():
                eval_stats_plot_dict[feature_name] = {}
                # idx2label is sorted by frequency already

                confusion_matrix = stats_dict.get("confusion_matrix")
                per_class_stats = stats_dict.get("per_class_stats")
                roc_curve = stats_dict.get("roc_curve")

                if confusion_matrix:
                    idx2str = meta_data[feature_name].get("idx2str")
                    idx2str = idx2str if idx2str else ["False", "True"]
                    eval_stats_plot_dict[feature_name]["confusion_matrix"] = make_confusion_matrix_plot(
                        confusion_matrix, feature_name, idx2str, per_class_stats)

                    str2idx = meta_data[feature_name].get('str2idx')
                    str2freq = meta_data[feature_name].get('str2freq')

                    if str2idx:
                        eval_stats_plot_dict[feature_name]["f1_score"] = make_f1_score_plot(
                            str2idx, str2freq, idx2str, per_class_stats)

                if roc_curve:
                    eval_stats_plot_dict[feature_name]["roc_curve"] = make_roc_curve(
                        roc_curve, feature_name)
            return eval_stats_plot_dict

        def _make_learning_curves_dict(train_stats) -> dict:
            # initialize
            import plotly.graph_objects as go
            from plotly.subplots import make_subplots
            import plotly
            colors = plotly.colors.DEFAULT_PLOTLY_COLORS
            learning_curves_dict = {}
            # stats are Ordered dict
            epoch = None
            for eval_split_index, (eval_split, stats_dict) in enumerate(train_stats.items()):
                for feature_name, metric_dict in stats_dict.items():
                    showlegend = True
                    subplots = learning_curves_dict.get(feature_name)
                    if subplots is None:
                        subplots = go.FigureWidget(
                            make_subplots(rows=1, cols=len(metric_dict), x_title="epochs", subplot_titles=tuple(metric_name for metric_name in metric_dict.keys())))
                        learning_curves_dict[feature_name] = subplots
                        subplots.update_layout(
                            title_text="출력 데이터 : "+feature_name)
                    for metric_index, metric in enumerate(metric_dict.values(), start=1):
                        if epoch is None:
                            epoch = [epoch+1 for epoch in range(len(metric))]
                        subplots.add_trace(go.Scatter(x=epoch, y=metric, name=eval_split, mode="lines", legendgroup=eval_split,
                                                    line_color=colors[eval_split_index], showlegend=showlegend), row=1, col=metric_index)
                        showlegend = False

            return learning_curves_dict

        self.learning_curves = _make_learning_curves_dict(train_stats)
        self.eval_plots = make_eval_stats_plot_dict(eval_stats, meta_data)
        import ipywidgets as widgets
        plot_list = []
        for _, figure_widget in self.learning_curves.items():
            plot_list.append(figure_widget)
        for _, metric_dict in self.eval_plots.items():
            for _, metric_figure in metric_dict.items():
                plot_list.append(metric_figure)
        return widgets.VBox(plot_list)


class TabularTrainingOptions(BaseCard):
    def __init__(
        self, 
        app_context:object = None,
        context_key:str = "",
        title:str = "",
        **kwargs,
        ):   

        self.app_context = app_context
        self.data = app_context.tabular_dataset.current_data
    
        self.style = {
            'column_options_body': "padding:0px;",
            'column_options_body_item': "min-height:62px; padding:0", 
        }

        # re-structure data for column-wise configuration
        num_rows = len(self.data.columns)
        self.config= self.app_context.training_params['ludwig']['config']

        # column options header ----------------------------------------------------------
        column_options_header_texts = [
            {"name":"입/출력", "style":"max-width:68px; text-align:center;"},
            {"name":"칼럼명", "style":"text-align:left; padding-left:40px; max-width:200px;"},
            {"name":"데이터 유형", "style":"min-width:327px; text-align:left;"},
        ]
        column_options_header = v.Row(
            style_ = "margin: 0px; width:100%; max-height:33px; padding:0 12px; background-color:#f1f1f1; border-top:1px solid #e0e0e0;",
            children = [
                v.Col(
                    style_ = 'font-size: 0.875rem; color:rgb(100, 116, 139); padding:0px;' + text['style'],
                    children = [text['name']],
                    ) for text in column_options_header_texts] 
        )

        # column options body -------------------------------------------------------------

        # reset data options body_rows when data is changed
        def _ignore_data_row(index):
            self.data_types[index].items = []
            self.data_types[index].v_model = None
            self.encoder_or_model_types[index].items = []
            self.encoder_or_model_types[index].v_model = None
            self.column_options_rows[index].children[5].children = []

        def _change_additional_options(index: int):
            in_out_ignore = self.in_out_ignore_buttons[index].v_slots[0]['children'][0].state
            data_type = self.data_types[index].v_model
            encoder_or_model_type = self.encoder_or_model_types[index].v_model
            additional_option_dict = _get_additional_option(in_out_ignore, data_type, encoder_or_model_type)
            self.column_options_rows[index].children[5].children = _make_additional_option_widget_row(index, additional_option_dict)

        def _change_encoder_or_model_type(index: int):
            in_out_ignore = self.in_out_ignore_buttons[index].v_slots[0]['children'][0].state
            data_type = self.data_types[index].v_model
            encoder_or_model_type = "encoder" if in_out_ignore == "input" else "model_type"

            self.encoder_or_model_types[index].items = self.config[in_out_ignore][encoder_or_model_type][data_type]['values'] 
            self.encoder_or_model_types[index].v_model = self.config[in_out_ignore][encoder_or_model_type][data_type]['default'] 
            self.encoder_or_model_types[index].readonly = True if len(self.encoder_or_model_types[index].items) == 1 else False

            _change_additional_options(index)

        def _change_data_types(index: int):
            in_out_ingore = self.in_out_ignore_buttons[index].v_slots[0]['children'][0].state
            pandas_data_type = pandas_data_types[index].v_model

            self.data_types[index].items = self.config[in_out_ingore]['dtype'][pandas_data_type]['values']
            self.data_types[index].v_model = self.config[in_out_ingore]['dtype'][pandas_data_type]['default']
            self.data_types[index].readonly = True if len(self.data_types[index].items) == 1 else False

            _change_encoder_or_model_type(index)

        # (1) in_out_ignore buttons ---------------------------------------------
        def _on_click_in_out_ignore(item, event=None, data=None):
            index = int(item.index)

            if item.state == 'input':
                new = {'state':'output', 'icon':'mdi-arrow-left-circle', 'text':"출력"}
            elif item.state == 'output':
                new = {'state':'ignore', 'icon':'mdi-close-circle', 'text':"제외"}
            else:
                new = {'state':'input', 'icon':'mdi-arrow-right-circle-outline', 'text':"입력"}

            # change state, icon & text
            item.state = new['state']
            item.children[0].children = [new['icon']]
            self.in_out_ignore_buttons[index].children = [new['text']]

            # change subordinate data
            if item.state != 'ignore':
                _change_data_types(index)
            else:
                _ignore_data_row(index)

            # check if output column is 
            train_ready = False
            for i in range(len(self.in_out_ignore_buttons)):
                if self.in_out_ignore_buttons[i].v_slots[0]['children'][0].state == 'output':
                    train_ready = True
                    break
            
            self.app_context.tabular_ai_training__train_activator.train_activator.disabled = not train_ready
            if train_ready:
                self.app_context.tabular_ai_training__train_activator.target_yn.hide()
            else:
                self.app_context.tabular_ai_training__train_activator.target_yn.show()

        def _make_tooltip_button(index):
            btn = StatedBtn(
                index = index,
                state = 'input',
                v_on='tooltip.on',
                icon = True,
                style_ = "margin-left:24px; margin-top:14px; margin-right:22px;",
                children = [v.Icon(children = "mdi-arrow-right-circle-outline")],
            )
            btn.on_event('click', _on_click_in_out_ignore)
            return btn

        self.in_out_ignore_buttons = [
            v.Tooltip(
                class_ = "in_out_ignore",
                right=True, 
                v_slots=[{
                    'name': 'activator',
                    'variable': 'tooltip',
                    'children': [_make_tooltip_button(str(i))],
                }],
                children = ['입력']
            ) for i in range(num_rows)
        ]

        # (2) column_names ------------------------------------------------------
        self.column_names = [
            v.Col(
                class_ = 'col_name',
                children = [column_name],
                style_ = "font-size:1rem; padding-top:22px; padding-bottom:5px; padding-right:15px; max-width:200px; min-width:200px; \
                    white-space:nowrap; overflow:hidden; text-overflow:ellipsis;",
            ) for column_name in self.data.columns
        ]

        # (3) pandas_data_types -------------------------------------------------
        pandas_data_types = [
            v.TextField(
                class_ = "pandas_dtype",
                v_model = dtype,
                style_ = "display:none;",
            ) for i, dtype in enumerate(self.data.dtypes.apply(lambda x: x.name).to_list())
            
        ]

        # (4) data_type for training -------------------------------------------------
        self.data_types = [
            DataSelect(
                index = str(i),
                class_ = "data_type",
                items = self.config['input']['dtype'][dtype.v_model]['values'],
                v_model = self.config['input']['dtype'][dtype.v_model]['default'],
                dense = True,
                style_ = "max-width:150px; margin-right:24px;",
                readonly = True if len(self.config['input']['dtype'][dtype.v_model]['values']) == 1 else False
            ) for i, dtype in enumerate(pandas_data_types)
        ]

        def _on_select_data_type(item, event=None, data=None):
            index = int(item.index)
            _change_encoder_or_model_type(index)

        for item in self.data_types:
            item.on_event('change', _on_select_data_type)

        # (5) input: encoder / output: model type--------------------------------
        self.encoder_or_model_types = [
            DataSelect(
                index = str(i),
                class_ = "encoder_or_model_type",
                items = self.config['input']['encoder'][dtype.v_model]['values'],
                v_model = self.config['input']['encoder'][dtype.v_model]['default'],
                dense = True,
                style_ = "max-width:150px; margin-right:24px;",
                readonly = True if len(self.config['input']['encoder'][dtype.v_model]['values']) == 1 else False
            ) for i, dtype in enumerate(self.data_types)
        ]

        def _on_select_encoder_or_model_type(item, event=None, data=None):
            index = int(item.index)
            _change_additional_options(index)

        for item in self.encoder_or_model_types:
           item.on_event('change', _on_select_encoder_or_model_type)

        # (6) additional options--------------------------------
        def _get_additional_option(in_out_ignore, data_type, encoder_or_model_type):
            return self.config[in_out_ignore]['additional_config'][data_type][encoder_or_model_type]

        def _make_additional_option_widget_row(index, additional_option_dict):
            self.additional_option_widgets = []
            for additional_option in additional_option_dict.items():
                if additional_option[0] == 'activation':
                    widget = LabeledSelect(
                        class_ = additional_option[0],
                        index = str(index),
                        label = "활성 함수",
                        items = additional_option[1]['values'],
                        v_model = additional_option[1]['default'],
                        dense = True,
                        style_ = "max-width:220px; padding: 0; margin: 3px !important; \
                            border-radius: 8px; background-color: #f1f1f1;",
                        readonly = True if len(additional_option[1]['values']) == 1 else False,
                    )
                    self.additional_option_widgets.append(widget)

                if additional_option[0] == 'representation':
                    widget = LabeledSelect(
                        class_ = additional_option[0],
                        index = str(index),
                        label = "표현 방식",
                        items = additional_option[1]['values'],
                        v_model = additional_option[1]['default'],
                        dense = True,
                        style_ = "max-width:220px; padding: 0; margin: 3px !important; \
                            border-radius: 8px; background-color: #f1f1f1;",
                        readonly = True if len(additional_option[1]['values']) == 1 else False,
                    )
                    self.additional_option_widgets.append(widget)
                
                if additional_option[0] == 'num_fc_layers':
                    widget = DataSlider(
                        class_ = additional_option[0],
                        index = str(index),
                        label = "FC 레이어 수",
                        range = additional_option[1],
                        dense = True,
                        style_ = "max-width:220px; padding: 0; margin: 3px !important; \
                            border-radius: 8px; background-color: #f1f1f1;",
                    )
                    self.additional_option_widgets.append(widget)
                
                if additional_option[0] == 'fc_size':
                    widget = DataSlider(
                        class_ = additional_option[0],
                        index = str(index),
                        label = "FC 크기",
                        range = additional_option[1],
                        dense = True,
                        style_ = "max-width:220px; padding: 0; margin: 3px !important; \
                            border-radius: 8px; background-color: #f1f1f1;",
                    )
                    self.additional_option_widgets.append(widget)

                if additional_option[0] == 'embedding_size':
                    widget = DataSlider(
                        class_ = additional_option[0],
                        index = str(index),
                        label = "임베딩 크기",
                        range = additional_option[1],
                        dense = True,
                        style_ = "max-width:220px; padding: 0; margin: 3px !important; \
                            border-radius: 8px; background-color: #f1f1f1;",
                    )
                    self.additional_option_widgets.append(widget)

                if additional_option[0] == 'dropout':
                    widget = DataSlider(
                        class_ = additional_option[0],
                        index = str(index),
                        label = "드롭 아웃",
                        range = additional_option[1],
                        dense = True,
                        style_ = "max-width:220px; padding: 0; margin: 3px !important; \
                            border-radius: 8px; background-color: #f1f1f1;",
                    )
                    self.additional_option_widgets.append(widget)
            return self.additional_option_widgets
        
        self.additional_option_rows =  [_get_additional_option(            
            in_out_ignore_button.v_slots[0]['children'][0].state, 
            data_type_option.v_model, 
            encoder_or_model_type.v_model
            ) for in_out_ignore_button, data_type_option, encoder_or_model_type in zip(self.in_out_ignore_buttons, self.data_types, self.encoder_or_model_types)
        ]

        self.additional_option_widget_rows = []
        for i, additional_option_dict in enumerate(self.additional_option_rows):
            self.additional_option_widget_rows.append(_make_additional_option_widget_row(i, additional_option_dict))
  
#-------------------------------------------------------------------------------
        self.column_options_rows = [
            IndexRow(
                index = str(i),
                children = [
                    self.in_out_ignore_buttons[i], 
                    self.column_names[i], 
                    pandas_data_types[i], 
                    self.data_types[i], 
                    self.encoder_or_model_types[i],
                    v.Row(
                        class_ = 'additional_options',
                        children =  self.additional_option_widget_rows[i],
                        style_ = "margin:0;",
                        ),
                ],
                style_ = "min-height:61px; margin:0;",
            ) for i in range(num_rows)

        ]       

        self.last_clicked_column_options_rows = None
        def _on_click_column_options_rows(item, event=None, data=None):
            index = int(item.index)
            if self.last_clicked_column_options_rows != index:
                self.last_clicked_column_options_rows = index
                self.app_context.tabular_ai_training__column_summary.update_data(self.data[self.column_names[index].children[0]])

        for row in self.column_options_rows:
            row.on_event('click', _on_click_column_options_rows)      


        self.column_options_body = v.List(
            class_ = context_key,
            style_ = self.style['column_options_body'],
            children = [
                v.ListItem(
                    class_ = "training-option-table-row",
                    children = [row],
                    dense = True,
                    style_ = self.style['column_options_body_item'],
                ) for row in self.column_options_rows
            ],    
        )

        self.column_options_body.children[-1].style_ = "border-bottom:0px; padding:0"


        # train parameter
        epochs = SmallHeaderCard(
            title = "Epochs",
            body = SimpleSlider(
                        range = [1, 1024, 1, 100],
                    ),
            size = {"width":"260px"}, 
        ) 

        batch_size = SmallHeaderCard(
            title = "Batch Size",
            body = SimpleSlider(
                        range = [1, 1024, 1, 128],
                    ),
            size = {"width":"260px"}, 
        ) 

        early_stop = SmallHeaderCard(
            title = "Early Stop",
            body = SimpleSlider(
                        range = [1, 1000, 1, 5],
                    ),
            size = {"width":"260px"}, 
        ) 

        optimizer = SmallHeaderCard(
            title = "Optimizer",
            body = v.Select(
                        v_model = "adam",
                        items = ['adam', 'rmsprop', 'sgd'],
                        dense = True,
                        style_ = "padding-left:16px;"
                    ),
            size = {"width":"260px"}, 
        ) 

        learning_rate = SmallHeaderCard(
            title = "Learning Rate",
            body = v.TextField(
                        v_model = 0.001,
                        dense = True,
                        style_ = "padding-left:16px;"
                    ),
            size = {"width":"260px"}, 
        ) 

        self.train_parameter = v.Row(
            children = [epochs, batch_size, early_stop, optimizer, learning_rate],
            style_ = "margin:0; height:100%; \
                justify-content: space-around; align-items: center;",
        )

        super().__init__(
            class_ = context_key,
            header_title_main = title,
            header_bottom  = column_options_header,
            body_items = [
                self.column_options_body, 
                # v.Spacer(style_ = "height:9px; background-color: rgb(241, 245, 249);"),
                self.train_parameter
                ],
            body_size = {
                "width":"1570px",
                "height":["340px", "100px"],
                    },
            body_border_bottom = [True, True],
            body_background_color = ["rgb(255, 255, 255)", "rgb(248, 250, 252)"],
            align = 'center',
            app_context = self.app_context,
        )


    def retrieve_config(self) -> dict: 
        self.train_config = {
            "input_features": [],
            "combiner": {"type":"concat"},
            "output_features": [],
            "preprocessing": {"numerical":{"normalization":"zscore"}},
            "training": {
                "epochs": None,
                "batch_size": None,
                "early_stop": None,
                "optimizer": {"type": "adam"},
                "learning_rate": None,
            },
        }

        def _get_additional_option_config(row):
            additional_option_config = {}
            for widget in row.children[-1].children:
                additional_option_config.update(
                    {widget.class_: widget.children[0].children[1].v_model}
                    )

            return additional_option_config

        for row in self.column_options_rows:
            additional_option_config = _get_additional_option_config(row)

            config_type = []
            if row.children[0].children[0] == "입력":
                config_type = ["input_features", "encoder"]
            elif row.children[0].children[0] == "출력":
                config_type = ["output_features", "decoder"]

            if not config_type == []:
                self.train_config[config_type[0]].append(
                    {
                        "name": row.children[1].children[0],
                        "type": row.children[3].v_model,
                        config_type[1]: row.children[4].v_model,
                        **additional_option_config
                    }
                )

        self.train_config["training"]["epochs"] = self.train_parameter.children[0].children[1].children[0].children[1].v_model
        self.train_config["training"]["batch_size"] = self.train_parameter.children[1].children[1].children[0].children[1].v_model
        self.train_config["training"]["early_stop"] = self.train_parameter.children[2].children[1].children[0].children[1].v_model
        self.train_config["training"]["optimizer"]["type"] = self.train_parameter.children[3].children[1].children[0].v_model
        self.train_config["training"]["learning_rate"] = self.train_parameter.children[4].children[1].children[0].v_model

        return self.train_config

    def save_config(self, path: str):
        config_path_to_save = os.path.join(path, "training_config_for_model_input.json")

        with open(config_path_to_save, 'w') as f:
            json.dump(self.retrieve_config(), f, indent=4)

    def retrieve_training_options(self):
        training_options = []
        training_options_row = {
            'column_options':[],
            'hyperparameter_options':[]
        }
        for row in self.column_options_rows:
            for widget in row.children:
                if widget.class_ == 'in_out_ignore':
                    option = {
                        'tooltip': widget.children[0], # list  입력, 출력, 제외
                        'state': widget.v_slots[0]['children'][0].state, # str 'input', 'output', 'ignore'
                        'icon': widget.v_slots[0]['children'][0].children[0].children[0] # list 
                        }
                elif row.class_ in ['data_type', 'encoder_or_model_type']:
                    option = {
                        'items': widget.items,
                        'v_model': widget.v_model,
                    }
                elif row.class_ == 'additional_options':
                    for sub_widget in widget.children:
                        if sub_widget.__class__name__ == 'LabeledSelect':
                            option = {
                                'items': sub_widget.children[0],
                                'v_model': sub_widget.children[1].children[1].v_model,
                            }
                        elif sub_widget.__class__name__ == 'DataSlider':
                            option = {
                                'v_model': sub_widget.children[1].v_model,
                            }
                        training_options_row['column_options'].append(option)
                training_options_row['column_options'].append(option)
            training_options.append(training_options_row)
