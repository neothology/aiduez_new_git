from dataclasses import dataclass

@dataclass
class AppContext:

## common variabls for general use ##
    current_user: dict = None
    current_data: object = None
    current_workflow: str = None # "tabular_ai_modeling"

## area(layout) ##
    BackGround: object = None
    SideNav: object = None
    TopArea: object = None
    WorkArea: object = None

## data ##
    data_for_project: object = None
 

