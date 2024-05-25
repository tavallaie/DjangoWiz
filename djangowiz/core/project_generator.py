import os
import importlib
from typing import List, Dict, Any
from djangowiz.core.io_handler import IOHandler
from djangowiz.core.project_io_handler import ProjectIOHandler


class ProjectGenerator:
    def __init__(
        self,
        app_name: str,
        project_name: str,
        model_names: List[str],
        template_dir: str = None,
        config_file: str = None,
        repo_dir: str = None,
    ):
        self.app_name = app_name
        self.project_name = project_name
        self.model_names = model_names
        self.default_template_dir = os.path.join(
            os.path.dirname(__file__), "..", "repo", "templates"
        )
        self.template_dir = template_dir or (
            os.path.join(repo_dir, "templates")
            if repo_dir
            else self.default_template_dir
        )
        self.generator_dir = (
            os.path.join(repo_dir, "generators")
            if repo_dir
            else os.path.join(os.path.dirname(__file__), "..", "repo", "generators")
        )
        self.config_file = config_file or (
            os.path.join(repo_dir, "generators.yaml")
            if repo_dir
            else os.path.join(
                os.path.dirname(__file__), "..", "repo", "generators.yaml"
            )
        )
        self.default_config_file = os.path.join(
            os.path.dirname(__file__), "..", "repo", "generators.yaml"
        )
        self.generators: Dict[str, Dict[str, Any]] = {}

        self.io_handler = ProjectIOHandler(
            self.config_file,
            self.default_config_file,
            self.template_dir,
            self.default_template_dir,
            self.generator_dir,
        )

        self.load_generators(self.config_file)

    def load_generators(self, config_file: str):
        user_config = IOHandler.load_yaml(config_file)
        default_config = IOHandler.load_yaml(self.default_config_file)

        for name, generator_config in default_config.get("generators", {}).items():
            self.generators[name] = generator_config

        for name, generator_config in user_config.get("generators", {}).items():
            if name in self.generators:
                self.generators[name]["options"].update(
                    generator_config.get("options", {})
                )
            else:
                self.generators[name] = generator_config

        for name, generator_config in self.generators.items():
            for option, config in generator_config.get("options", {}).items():
                self.load_generator(name, option, config)

    def load_generator(self, name: str, option: str, config: Dict[str, Any]):
        class_path = config["class"]
        module_path, class_name = class_path.rsplit(".", 1)
        if self.generator_dir not in module_path:
            module_path = os.path.join(self.generator_dir, module_path)
        module = importlib.import_module(module_path)
        generator_class = getattr(module, class_name)
        template_path = config.get("template", "")

        if not os.path.exists(os.path.join(self.template_dir, template_path)):
            template_path = os.path.join(self.default_template_dir, template_path)

        self.generators[f"{name}_{option}"] = {
            "class": generator_class(
                self.app_name,
                self.project_name,
                self.model_names,
                self.template_dir,
                **config,
            ),
            "template": template_path,
        }

    def save_generators(self):
        combined_config = {"generators": {}}
        for name, generator in self.generators.items():
            base_name, option = name.rsplit("_", 1)
            if base_name not in combined_config["generators"]:
                combined_config["generators"][base_name] = {"options": {}}
            combined_config["generators"][base_name]["options"][option] = {
                "class": generator["class"].__class__.__module__
                + "."
                + generator["class"].__class__.__name__,
                "template": generator["template"],
                **{
                    k: v
                    for k, v in generator["class"].options.items()
                    if k not in ["class", "template"]
                },
            }

        IOHandler.save_yaml(combined_config, self.config_file)

    def add_generator(
        self, name: str, class_path: str, template_path: str, option: str, **kwargs
    ):
        generator_key = f"{name}_{option}"
        if generator_key in self.generators:
            print(
                f"Generator '{generator_key}' already exists. Use update_generator to update it."
            )
            return

        if not os.path.exists(template_path):
            template_path = os.path.join(self.default_template_dir, template_path)

        module_path, class_name = class_path.rsplit(".", 1)
        module = importlib.import_module(module_path)
        generator_class = getattr(module, class_name)
        generator_instance = generator_class(
            self.app_name,
            self.project_name,
            self.model_names,
            self.template_dir,
            **kwargs,
        )

        self.generators[generator_key] = {
            "class": generator_instance,
            "template": template_path,
        }

        self.save_generators()
        IOHandler.copy_file(
            module_path.replace(".", "/") + ".py",
            os.path.join(self.generator_dir, module_path.replace(".", "/") + ".py"),
        )
        self.load_generators(self.config_file)  # Reload configuration
        print(f"Generator '{generator_key}' has been added.")

    def delete_generator(self, name: str, option: str):
        generator_key = f"{name}_{option}"
        if generator_key in self.generators:
            IOHandler.remove_file(
                self.generators[generator_key]["class"].__module__.replace(".", "/")
                + ".py"
            )
            del self.generators[generator_key]
            self.save_generators()
            self.load_generators(self.config_file)  # Reload configuration
            print(f"Generator '{generator_key}' has been deleted.")
        else:
            print(f"Generator '{generator_key}' does not exist.")

    def update_generator(
        self, name: str, class_path: str, template_path: str, option: str, **kwargs
    ):
        generator_key = f"{name}_{option}"
        if not os.path.exists(template_path):
            template_path = os.path.join(self.default_template_dir, template_path)

        module_path, class_name = class_path.rsplit(".", 1)
        module = importlib.import_module(module_path)
        generator_class = getattr(module, class_name)
        generator_instance = generator_class(
            self.app_name,
            self.project_name,
            self.model_names,
            self.template_dir,
            **kwargs,
        )

        self.generators[generator_key] = {
            "class": generator_instance,
            "template": template_path,
        }

        self.save_generators()
        IOHandler.copy_file(
            module_path.replace(".", "/") + ".py",
            os.path.join(self.generator_dir, module_path.replace(".", "/") + ".py"),
        )
        self.load_generators(self.config_file)  # Reload configuration
        print(f"Generator '{generator_key}' has been updated.")

    def show_generators(self):
        for name, generator in self.generators.items():
            print(
                f"Generator: {name} ({generator['class'].__class__.__module__}.{generator['class'].__class__.__name__}), Template: {generator['template']}, Config: {generator['class'].options}"
            )

    def generate(
        self, components: List[str], option: str, overwrite: bool = False, **kwargs
    ):
        for component in components:
            generator_key = f"{component}_{option}"
            if generator_key in self.generators:
                generator = self.generators[generator_key]["class"]
                template = self.generators[generator_key]["template"]
                generator.generate(overwrite=overwrite, template=template, **kwargs)

    def export_config(self, export_path: str):
        self.io_handler.export_config(export_path)

    def import_config(self, import_path: str):
        self.io_handler.import_config(import_path)
