import os
import shutil
import yaml
from typing import Dict, Any


class IOHandler:
    @staticmethod
    def load_yaml(file_path: str) -> Dict[str, Any]:
        with open(file_path, "r") as file:
            return yaml.safe_load(file)

    @staticmethod
    def save_yaml(data: Dict[str, Any], file_path: str):
        with open(file_path, "w") as file:
            yaml.safe_dump(data, file)

    @staticmethod
    def copy_file(src: str, dst: str):
        os.makedirs(os.path.dirname(dst), exist_ok=True)
        shutil.copy(src, dst)

    @staticmethod
    def copy_tree(src: str, dst: str, dirs_exist_ok: bool = True):
        shutil.copytree(src, dst, dirs_exist_ok=dirs_exist_ok)

    @staticmethod
    def remove_file(file_path: str):
        if os.path.exists(file_path):
            os.remove(file_path)
