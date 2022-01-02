from dataclasses import dataclass

@dataclass
class AppConfig:
    side_nav_menu: dict = None
    class_paths: dict = None
    workflows: dict = None
    
