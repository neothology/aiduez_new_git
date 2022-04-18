from dataclasses import dataclass
from utils import read_config

@dataclass
class AppContext:

## set env as dev or prod
    env: str = None

## config variables necessary when initialization
    theme: str = None

## current variables
    current_user: str = None
    current_workflow: str = None
    current_workflow_stage: str = None
    current_workflow_stage_sub: str = None
    current_workbook: object = None

## for control
    ignore_progress_linear: bool = False

## base layout object ##
    background: object = None
    alert: object = None
    side_nav: object = None
    side_nav_menu: object = None
    list_menu_sub: object = None
    top_area: object = None
    work_area: object = None
    base_overlay: object = None
    progress_linear: object = None

## workbook list ##
    workbooks: dict = None

## workflow stages object ##
    # --------------------------------------------------
    task_recent: object = None
    task_recent_view: object = None
    task_favorite: object = None
    task_favorite_view: object = None
    task_all_view: object = None
    task_all: object = None

    tabular_base: object = None
    tabular_dataset: object = None
    tabular_model: object = None

    tabular_tab_menu: object = None
    tabular_contents: object = None
    tabular_data_context: object = None
    tabular_model: object = None
    tabular_dataset: object = None

    # tabular data import objects
    tabular_data_import: object = None
    tabular_data_import__sub_menu: object = None
    tabular_data_import__sub_contents: object = None
    tabular_data_import__workbook_data_list_view: object = None
    tabular_data_import__workbook_aidu_list_view: object = None
    tabular_import_pc: object = None
    tabular_import_pc_view: object = None
    tabular_import_aidu: object = None
    tabular_import_aidu_view: object = None
    tabular_import_edap: object = None
    tabular_import_edap_view: object = None

    # tabular data analytics objects
    tabular_data_analytics: object = None
    tabular_data_analytics__sub_menu: object = None
    tabular_data_analytics__sub_contents: object = None
    tabular_data_analytics_options: object = None

    tabular_analytics_basicinfo: object = None
    tabular_analytics_basicinfo_view: object = None

    tabular_analytics_scatter: object = None
    tabular_analytics_scatter_view: object = None
    tabular_analytics_heatmap: object = None
    tabular_analytics_heatmap_view: object = None
    tabular_analytics_boxplot: object = None
    tabular_analytics_boxplot_view: object = None
    tabular_analytics_density: object = None
    tabular_analytics_density_view: object = None

    tabular_analytics_wcloud: object = None
    tabular_analytics_wcloud_view: object = None

    tabular_analytics_reduction: object = None
    tabular_analytics_reduction_view: object = None
    tabular_analytics_clustering: object = None
    tabular_analytics_clustering_view: object = None
    tabular_analytics_datasample: object = None
    tabular_analytics_datasample_view: object = None

    #tabular data processing objects
    tabular_data_processing: object = None
    tabular_data_processing__changed: bool = False
    tabular_data_processing__save_activator: object = None
    tabular_data_processing__sub_menu: object = None
    tabular_data_processing__sub_contents: object = None
    tabular_data_processing__column_summary: object = None
    tabular_data_single_processing_view: object = None
    tabular_data_single_processing_dialog_view: object = None
    tabular_data_multiple_processing_view: object = None

    # tabilar ai training objects
    tabular_ai_training: object = None
    tabular_ai_training__train_activator: object = None
    tabular_ai_training__training_options: object = None
    tabular_ai_training__column_summary: object = None
    tabular_ai_training__train_result: object = None
    tabular_ai_training__progress_linear: object = None

    tabular_ai_evaluation: object = None
    # --------------------------------------------------
    text_base: object = None
    text_tab_menu: object = None
    text_contents: object = None

    text_data_import: object = None
    text_data_analytics: object = None
    text_ai_training: object = None
    text_ai_evaluation: object = None
    # --------------------------------------------------

    image_base: object = None
    image_tab_menu: object = None
    image_contents: object = None

    image_data_import: object = None
    image_data_analytics: object = None
    image_ai_training: object = None
    image_ai_evaluation: object = None
    # --------------------------------------------------

    audio_base: object = None
    audio_tab_menu: object = None
    audio_contents: object = None

    audio_data_import: object = None
    audio_data_analytics: object = None
    audio_ai_training: object = None
    audio_ai_evaluation: object = None
    # --------------------------------------------------

    video_base: object = None
    video_tab_menu: object = None
    video_contents: object = None

    video_data_import: object = None
    video_data_analytics: object = None
    video_ai_training: object = None
    video_ai_evaluation: object = None

    def __post_init__(self):

        # set config from aiduez_config.yml
        app_config = read_config()
        
        # re-assign config values to context variables for better readability
        self.class_paths: dict = app_config["class_paths"]
        self.side_nav_menu_list: dict = app_config['side_nav_menu_list']
        self.workflows_list: dict = app_config['workflows_list']
        self.theme_values: dict = app_config['theme'][self.theme]
        self.env_values: dict = app_config['envs']
        self.processing_params: dict = app_config['processing_params']
        self.training_params: dict = app_config['training_params']
        self.workbook_icons: list = app_config['workbook_icons']
        self.workbook_colors: list = app_config['workbook_colors']

    def clear_workflow(self):
        self.workflow_base = None
        self.workflow_tab_menu = None
        self.workflow_contents = None
        self.workflow_data_import = None
        self.workflow_data_import__sub_menu = None
        self.workflow_data_import__sub_contents = None
        self.workflow_data_import__workbook_data_list = None
        self.workflow_data_import__workbook_aidu_list = None
        self.workflow_import_pc = None
        self.workflow_import_pc_view = None
        self.workflow_import_aidu = None
        self.workflow_import_aidu_view = None
        self.workflow_import_edap = None
        self.workflow_import_edap_view = None
        self.workflow_data_analytics = None
        self.workflow_data_analytics__sub_menu = None
        self.workflow_data_analytics__sub_contents = None
        self.workflow_data_analytics_options = None
        self.workflow_analytics_basicinfo = None
        self.workflow_analytics_basicinfo__data_info = None
        self.workflow_analytics_basicinfo__column_summary_simple = None
        self.workflow_analytics_scatter = None
        self.workflow_analytics_scatter_view = None
        self.workflow_analytics_heatmap = None
        self.workflow_analytics_heatmap_view = None
        self.workflow_analytics_boxplot = None
        self.workflow_analytics_boxplot_view = None
        self.workflow_analytics_density = None
        self.workflow_analytics_density_view = None
        self.workflow_analytics_wcloud = None
        self.workflow_analytics_wcloud_view = None
        self.workflow_analytics_reduction = None
        self.workflow_analytics_reduction_view = None
        self.work