from nntplib import NNTPPermanentError
import os
import re
import zipfile
import ipyvuetify as v
from utils import get_or_create_class, delete_files_in_dir
from dataclasses import dataclass, field

@dataclass
class WorkBookProfile:
    type: str = None
    name: str = None
    path: str = None
    list_works: list = None
    list_data: list = None
    list_models: list = None
    size: int = None
    icon: str = None
    color: str = None
    favoraite: bool = None
    desc: str = None

@dataclass
class Workbooks:

    workbook_names: list = field(default_factory=list)

    def load_workbooks(self, dir:str = ""):
        pass

