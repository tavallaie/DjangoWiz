import os
import ast
from jinja2 import Environment, FileSystemLoader, ChoiceLoader
from typing import List


class ModelExtractor:
    @staticmethod
    def extract_model_names(file_path: str) -> List[str]:
        model_names = []
        with open(file_path, "r") as file:
            tree = ast.parse(file.read(), filename=file_path)
        for node in ast.walk(tree):
            if isinstance(node, ast.ClassDef):
                bases = [
                    base.id if isinstance(base, ast.Name) else base.attr
                    for base in node.bases
                ]
                if "Model" in bases or any(base for base in bases):
                    model_names.append(node.name)
        return model_names


class ProjectGenerator:
    def __init__(
        self,
        app_name: str,
        project_name: str,
        model_names: List[str],
        template_dir: str = None,
    ):
        self.app_name = app_name
        self.project_name = project_name
        self.model_names = model_names

        # Use default template directory if no custom template directory is provided
        default_template_dir = os.path.join(os.path.dirname(__file__), "templates")
        loaders = [FileSystemLoader(default_template_dir)]
        if template_dir:
            loaders.insert(0, FileSystemLoader(template_dir))
        self.env = Environment(loader=ChoiceLoader(loaders))

    def write_file(self, file_path: str, content: str, overwrite: bool = False):
        if not overwrite and os.path.exists(file_path):
            print(f"Skipping existing file: {file_path}")
            return
        os.makedirs(os.path.dirname(file_path), exist_ok=True)
        with open(file_path, "w") as file:
            file.write(content)
        print(f"Generated file: {file_path}")

    def generate_serializers(self, single_file: bool, overwrite: bool = False):
        if single_file:
            imports = f'from rest_framework import serializers\nfrom {self.app_name}.models import {", ".join(self.model_names)}\n\n'
            template = self.env.get_template("single/serializers.py.j2")
            content = imports + template.render(
                app_name=self.app_name, model_names=self.model_names
            )
            self.write_file(
                os.path.join(self.app_name, "serializers.py"), content, overwrite
            )
        else:
            for model_name in self.model_names:
                template = self.env.get_template("multi/serializers.py.j2")
                content = template.render(app_name=self.app_name, model_name=model_name)
                self.write_file(
                    os.path.join(
                        self.app_name, "serializers", f"{model_name.lower()}.py"
                    ),
                    content,
                    overwrite,
                )
            serializer_init_content = "\n".join(
                [
                    f"from .{model_name.lower()} import {model_name}Serializer"
                    for model_name in self.model_names
                ]
            )
            self.write_file(
                os.path.join(self.app_name, "serializers", "__init__.py"),
                serializer_init_content,
                overwrite,
            )

    def generate_viewsets(self, single_file: bool, overwrite: bool = False):
        if single_file:
            model_imports = f'from rest_framework import generics\nfrom {self.app_name}.models import {", ".join(self.model_names)}\n'
            serializer_imports = f'from {self.app_name}.serializers import {", ".join([model_name + "Serializer" for model_name in self.model_names])}\n\n'
            template = self.env.get_template("single/viewsets.py.j2")
            content = (
                model_imports
                + serializer_imports
                + template.render(app_name=self.app_name, model_names=self.model_names)
            )
            self.write_file(
                os.path.join(self.app_name, "viewsets.py"), content, overwrite
            )
        else:
            for model_name in self.model_names:
                template = self.env.get_template("multi/viewsets.py.j2")
                content = template.render(app_name=self.app_name, model_name=model_name)
                self.write_file(
                    os.path.join(self.app_name, "viewsets", f"{model_name.lower()}.py"),
                    content,
                    overwrite,
                )
            viewset_init_content = "\n".join(
                [
                    f"from .{model_name.lower()} import {model_name}ListCreateAPIView, {model_name}RetrieveUpdateDestroyAPIView"
                    for model_name in self.model_names
                ]
            )
            self.write_file(
                os.path.join(self.app_name, "viewsets", "__init__.py"),
                viewset_init_content,
                overwrite,
            )

    def generate_urls(self, overwrite: bool = False):
        template = self.env.get_template("urls.py.j2")
        content = template.render(app_name=self.app_name, model_names=self.model_names)
        self.write_file(os.path.join(self.app_name, "urls.py"), content, overwrite)

    def generate_routes(self, overwrite: bool = False):
        template = self.env.get_template("routes.py.j2")
        content = template.render(app_name=self.app_name, model_names=self.model_names)
        self.write_file(os.path.join(self.app_name, "routes.py"), content, overwrite)

    def generate_dockerfile(self, overwrite: bool = False):
        template = self.env.get_template("Dockerfile.j2")
        content = template.render(project_name=self.project_name)
        self.write_file("Dockerfile", content, overwrite)

    def generate_docker_compose(
        self, db_name: str, db_user: str, db_password: str, overwrite: bool = False
    ):
        for env in ["dev", "prod"]:
            template = self.env.get_template(f"docker-compose.{env}.yml.j2")
            content = template.render(
                db_name=db_name,
                db_user=db_user,
                db_password=db_password,
                project_name=self.project_name,
            )
            self.write_file(f"docker-compose.{env}.yml", content, overwrite)

    def generate_env_files(
        self, db_name: str, db_user: str, db_password: str, overwrite: bool = False
    ):
        for env in ["dev", "prod"]:
            template = self.env.get_template(f"env.{env}.j2")
            content = template.render(
                db_name=db_name, db_user=db_user, db_password=db_password
            )
            self.write_file(f".env.{env}", content, overwrite)

    def generate_all(self, single_file: bool, overwrite: bool = False):
        self.generate_serializers(single_file, overwrite)
        self.generate_viewsets(single_file, overwrite)
        self.generate_urls(overwrite)
        self.generate_routes(overwrite)
        self.generate_dockerfile(overwrite)
        self.generate_docker_compose(
            db_name="your_db",
            db_user="your_user",
            db_password="your_password",
            overwrite=overwrite,
        )
        self.generate_env_files(
            db_name="your_db",
            db_user="your_user",
            db_password="your_password",
            overwrite=overwrite,
        )

    def generate_core_files(self, single_file: bool, overwrite: bool = False):
        self.generate_serializers(single_file, overwrite)
        self.generate_viewsets(single_file, overwrite)
        self.generate_routes(overwrite)
