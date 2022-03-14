from dataclasses import dataclass
from utils import read_config

@dataclass
class AppContext:

## set env as dev or prod
    env: str = None

## config variables necessary when initialization ##
    theme: str = None

## pipeline variables #
    current_work_file: object = None
    mf_experiment_id: str = None
    mf_experiment_name: str = None

## common variabls for general use ##
    current_user: dict = None
    current_data_name: str = ''
    current_data: object = None
    current_workflow: str = None

## base layout object ##
    background: object = None
    side_nav: object = None
    side_nav_menu: object = None
    top_area: object = None
    work_area: object = None

## workflow stages object ##
    # --------------------------------------------------
    tabular_base: object = None
    tabular_tab_menu: object = None
    tabular_contents: object = None
    tabular_workflow_stage: str = None

    # tabular data import objects
    tabular_data_import: object = None
    tabular_data_import_tab: object = None
    tabular_data_import_aidu: object = None
    tabular_data_import_local: object = None
    tabular_data_import_edap: object = None
    tabular_data_import_pod: object = None

    # tabular data analyze objects
    tabular_data_analyze: object = None

    # tabilar ai training objects
    tabular_ai_training: object = None
    tabular_ai_training__modeling_options: object = None
    tabular_ai_training__column_summary: object = None

    tabular_ai_evaluation: object = None
    # --------------------------------------------------
    text_base: object = None
    text_tab_menu: object = None
    text_contents: object = None
    text_workflow_stage: str = None

    text_data_import: object = None
    text_data_analyze: object = None
    text_ai_training: object = None
    text_ai_evaluation: object = None
    # --------------------------------------------------

    image_base: object = None
    image_tab_menu: object = None
    image_contents: object = None
    image_workflow_stage: str = None

    image_data_import: object = None
    image_data_analyze: object = None
    image_ai_training: object = None
    image_ai_evaluation: object = None
    # --------------------------------------------------

    audio_base: object = None
    audio_tab_menu: object = None
    audio_contents: object = None
    audio_workflow_stage: str = None

    audio_data_import: object = None
    audio_data_analyze: object = None
    audio_ai_training: object = None
    audio_ai_evaluation: object = None
    # --------------------------------------------------

    video_base: object = None
    video_tab_menu: object = None
    video_contents: object = None
    video_workflow_stage: str = None

    video_data_import: object = None
    video_data_analyze: object = None
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
        self.modeling_params: dict = app_config['modeling_params']

