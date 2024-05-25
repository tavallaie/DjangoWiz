# djangowiz/core/base_generator.py

from typing import List
from jinja2 import Environment, FileSystemLoader
import os


class BaseGenerator:
    def __init__(
        self,
        app_name: str,
        project_name: str,
        model_names: List[str],
        template_dir: str,
        **kwargs,
    ):
        self.app_name = app_name
        self.project_name = project_name
        self.model_names = model_names
        self.env = Environment(loader=FileSystemLoader(template_dir))
        self.options = kwargs

    def generate(self, overwrite: bool = False, template: str = None, **kwargs):
        raise NotImplementedError("Subclasses must implement this method")

    def render_template(self, template_name: str, context: dict) -> str:
        template = self.env.get_template(template_name)
        return template.render(context)

    def write_file(self, file_path: str, content: str, overwrite: bool = False):
        if not overwrite and os.path.exists(file_path):
            print(f"Skipping existing file: {file_path}")
            return
        os.makedirs(os.path.dirname(file_path), exist_ok=True)
        with open(file_path, "w") as file:
            file.write(content)
        print(f"Generated file: {file_path}")
