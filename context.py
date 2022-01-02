from dataclasses import dataclass

@dataclass
class AppContext:

## common variabls for general use ##
    current_user: dict = None
    current_data: object = None
    current_workflow: str = None
    current_workflow_stage: str = None

## area(layout) ##
    background: object = None
    side_nav: object = None
    side_nav_menu: object = None
    top_area: object = None
    work_area: object = None
    work_area_tab_menu: object = None
    work_area_contents: object = None

## workflow stages ##
    tabular_tab_menu: object = None
    tabular_contents: object = None
    tabular_base: object = None
    tabular_data_import: object = None
    tabular_data_analyze: object = None
    tabular_ai_training: object = None
    tabular_ai_evaluation: object = None

    text_base: object = None
    text_data_import: object = None
    text_data_analyze: object = None
    text_ai_training: object = None
    text_ai_evaluation: object = None

    image_base: object = None
    image_data_import: object = None
    image_data_analyze: object = None
    image_ai_training: object = None
    image_ai_evaluation: object = None

    audio_base: object = None
    audio_data_import: object = None
    audio_data_analyze: object = None
    audio_ai_training: object = None
    audio_ai_evaluation: object = None

    video_base: object = None
    video_data_import: object = None
    video_data_analyze: object = None
    video_ai_training: object = None
    video_ai_evaluation: object = None
    

