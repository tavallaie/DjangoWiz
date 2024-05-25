# djangowiz/app.py

import typer
import os
from typing import Optional, Dict, Any
import yaml
from djangowiz.core.project_generator import ProjectGenerator
from djangowiz.core.model_extractor import ModelExtractor


def create_app():
    app = typer.Typer()
    generate_app = typer.Typer()
    app.add_typer(generate_app, name="generate")

    def load_generators(config_file: str) -> Dict[str, Any]:
        print(f"Loading configuration from {config_file}")
        with open(config_file, "r") as file:
            return yaml.safe_load(file)

    def get_command_function(generator_name: str, option: str):
        def command_function(
            app_name: str,
            project_name: str,
            model_file: str,
            template_dir: Optional[str] = typer.Option(
                None, help="Custom template directory"
            ),
            config_file: Optional[str] = typer.Option(None, help="Custom config file"),
            repo_dir: Optional[str] = typer.Option(None, help="Custom repo directory"),
            overwrite: bool = typer.Option(False, help="Overwrite existing files"),
        ):
            model_names = ModelExtractor.extract_model_names(model_file)
            project_generator = ProjectGenerator(
                app_name, project_name, model_names, template_dir, config_file, repo_dir
            )
            project_generator.generate([generator_name], option, overwrite)

        return command_function

    def register_commands(config_file: str):
        generators = load_generators(config_file)
        # Handle the nested 'generators' key
        generator_configs = generators.get("generators", {})

        for generator_name, generator_config in generator_configs.items():
            for option, config in generator_config.get("options", {}).items():
                command_function = get_command_function(generator_name, option)
                option_name = f"{generator_name}-{option}"
                generate_app.command(name=option_name.replace("_", "-"))(
                    command_function
                )

    @app.command()
    def generate_files(
        app_name: str,
        project_name: str,
        model_file: str,
        template_dir: Optional[str] = typer.Option(None),
        config_file: Optional[str] = typer.Option(None),
        repo_dir: Optional[str] = typer.Option(None),
        single_file: bool = typer.Option(False),
        overwrite: bool = typer.Option(False),
    ):
        model_names = ModelExtractor.extract_model_names(model_file)
        project_generator = ProjectGenerator(
            app_name, project_name, model_names, template_dir, config_file, repo_dir
        )
        project_generator.generate(
            [
                "serializers",
                "viewsets",
                "urls",
                "routes",
                "dockerfile",
                "docker_compose",
                "env_files",
            ],
            "single" if single_file else "multi",
            overwrite,
        )

    register_commands(
        os.path.join(os.path.dirname(__file__), "repo", "generators.yaml")
    )
    return app


app = create_app()
