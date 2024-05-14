import os
import re
import typer
from jinja2 import Environment, FileSystemLoader
from typing import List

app = typer.Typer()


class ModelExtractor:
    @staticmethod
    def extract_model_names(model_file: str) -> List[str]:
        model_names = []
        with open(model_file, "r") as file:
            content = file.read()
        classes = re.findall(r"class\s+(\w+)\s*\(.*?\):", content)
        for class_name in classes:
            if re.search(rf"class\s+{class_name}\s*\(.*Model.*\):", content):
                model_names.append(class_name)
        return model_names


class ProjectGenerator:
    def __init__(self, app_name: str, project_name: str, model_names: List[str]):
        self.app_name = app_name
        self.project_name = project_name
        self.model_names = model_names
        self.env = Environment(loader=FileSystemLoader("DjangoWiz/templates"))

    def write_file(self, file_path: str, content: str, overwrite: bool = False):
        if not overwrite and os.path.exists(file_path):
            print(f"Skipping existing file: {file_path}")
            return
        os.makedirs(os.path.dirname(file_path), exist_ok=True)
        with open(file_path, "w") as file:
            file.write(content)
        print(f"Generated file: {file_path}")

    def generate_serializers(self, overwrite: bool = False):
        for model_name in self.model_names:
            template = self.env.get_template("serializer.py.j2")
            content = template.render(app_name=self.app_name, model_name=model_name)
            self.write_file(
                os.path.join(self.app_name, "serializers", f"{model_name.lower()}.py"),
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

    def generate_viewsets(self, overwrite: bool = False):
        for model_name in self.model_names:
            template = self.env.get_template("viewset.py.j2")
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

    def generate_all(self, overwrite: bool = False):
        self.generate_serializers(overwrite)
        self.generate_viewsets(overwrite)
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

    def generate_core_files(self, overwrite: bool = False):
        self.generate_serializers(overwrite)
        self.generate_viewsets(overwrite)
        self.generate_routes(overwrite)


@app.command()
def generate_files(
    app_name: str, project_name: str, model_file: str, overwrite: bool = False
):
    model_names = ModelExtractor.extract_model_names(model_file)
    generator = ProjectGenerator(app_name, project_name, model_names)
    generator.generate_all(overwrite)
    print(
        f"Files for {len(model_names)} models have been generated in the {app_name} directory."
    )


@app.command()
def generate_core_files(
    app_name: str, project_name: str, model_file: str, overwrite: bool = False
):
    model_names = ModelExtractor.extract_model_names(model_file)
    generator = ProjectGenerator(app_name, project_name, model_names)
    generator.generate_core_files(overwrite)
    print(
        f"Serializers, viewsets, and routes for {len(model_names)} models have been generated in the {app_name} directory."
    )


@app.command()
def generate_serializers(
    app_name: str, project_name: str, model_file: str, overwrite: bool = False
):
    model_names = ModelExtractor.extract_model_names(model_file)
    generator = ProjectGenerator(app_name, project_name, model_names)
    generator.generate_serializers(overwrite)
    print(
        f"Serializers for {len(model_names)} models have been generated in the {app_name} directory."
    )


@app.command()
def generate_viewsets(
    app_name: str, project_name: str, model_file: str, overwrite: bool = False
):
    model_names = ModelExtractor.extract_model_names(model_file)
    generator = ProjectGenerator(app_name, project_name, model_names)
    generator.generate_viewsets(overwrite)
    print(
        f"Viewsets for {len(model_names)} models have been generated in the {app_name} directory."
    )


@app.command()
def generate_urls(
    app_name: str, project_name: str, model_file: str, overwrite: bool = False
):
    model_names = ModelExtractor.extract_model_names(model_file)
    generator = ProjectGenerator(app_name, project_name, model_names)
    generator.generate_urls(overwrite)
    print(f"URLs have been generated in the {app_name} directory.")


@app.command()
def generate_routes(
    app_name: str, project_name: str, model_file: str, overwrite: bool = False
):
    model_names = ModelExtractor.extract_model_names(model_file)
    generator = ProjectGenerator(app_name, project_name, model_names)
    generator.generate_routes(overwrite)
    print(f"Routes have been generated in the {app_name} directory.")


if __name__ == "__main__":
    app()
