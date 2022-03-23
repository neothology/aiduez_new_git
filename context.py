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

## base layout object ##
    background: object = None
    side_nav: object = None
    side_nav_menu: object = None
    list_menu_sub: object = None
    top_area: object = None
    work_area: object = None
    base_overlay: object = None

## workflow stages object ##
    # --------------------------------------------------
    tabular_base: object = None
    tabular_workbook: object = None
    tabular_dataset: object = None
    tabular_model: object = None

    tabular_tab_menu: object = None
    tabular_contents: object = None
    tabular_data_context: object = None
    tabular_model: object = None
    tabular_dataset: object = None

    # tabular data import objects
    tabular_data_import: object = None
    tabular_data_import_tab: object = None
    tabular_data_import_aidu: object = None
    tabular_data_import_local: object = None
    tabular_data_import_edap: object = None
    tabular_data_import_pod: object = None

    

    # tabular data analytics objects
    tabular_data_analytics: object = None

    #tabular data processing objects
    tabular_data_processing: object = None
    tabular_data_processing_tab: object = None
    tabular_data_single_processing: object = None
    tabular_data_single_processing_dialog: object = None
    tabular_data_processing_column_summary: object = None

    # tabilar ai training objects
    tabular_ai_training: object = None
    tabular_ai_training__train_activator: object = None
    tabular_ai_training__training_options: object = None
    tabular_ai_training__column_summary: object = None
    tabular_ai_training__train_result: object = None

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

    
    
    # def createJob(self, currPjtName, data_name):
    #     self.info = [True, "작업 생성 완료"]