# djangowiz/cli.py

import typer
import os
from typing import Optional, Dict, Any, List
import yaml
from djangowiz.core.project_generator import ProjectGenerator
from djangowiz.core.model_extractor import ModelExtractor

app = typer.Typer()
generate_app = typer.Typer()
app.add_typer(generate_app, name="generate")

generators_config = {}


def load_generators(config_file: str) -> Dict[str, Any]:
    print(f"Loading configuration from {config_file}")
    with open(config_file, "r") as file:
        return yaml.safe_load(file)


def create_command_function(generator_name: str, options: Dict[str, Any]):
    def command_function(
        app_name: str,
        project_name: str,
        model_file: str,
        overwrite: bool = typer.Option(False, help="Overwrite existing files"),
        option: str = typer.Option(
            ..., help=f"Specify the generation option ({', '.join(options.keys())})"
        ),
        template_dir: Optional[str] = typer.Option(
            None, help="Custom template directory"
        ),
        config_file: Optional[str] = typer.Option(None, help="Custom config file"),
        repo_dir: Optional[str] = typer.Option(None, help="Custom repo directory"),
    ):
        model_names = ModelExtractor.extract_model_names(model_file)
        project_generator = ProjectGenerator(
            app_name,
            project_name,
            model_names,
            template_dir,
            config_file,
            repo_dir,
            model_file=model_file,
        )
        project_generator.generate([generator_name], option, overwrite)

    return command_function


def register_commands(config_file: str):
    global generators_config
    generators = load_generators(config_file)
    generators_config = generators.get("generators", {})
    for generator_name, generator_config in generators_config.items():
        options = generator_config.get("options", {})
        command_function = create_command_function(generator_name, options)
        generate_app.command(name=generator_name)(command_function)


@app.command()
def generate_files(
    app_name: str,
    project_name: str,
    model_file: str,
    overwrite: bool = typer.Option(False),
    option: str = typer.Option(..., help="Specify the generation option"),
    template_dir: Optional[str] = typer.Option(None),
    config_file: Optional[str] = typer.Option(None),
    repo_dir: Optional[str] = typer.Option(None),
):
    model_names = ModelExtractor.extract_model_names(model_file)
    project_generator = ProjectGenerator(
        app_name,
        project_name,
        model_names,
        template_dir,
        config_file,
        repo_dir,
        model_file=model_file,
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
        option,
        overwrite,
    )


register_commands(os.path.join(os.path.dirname(__file__), "repo", "generators.yaml"))

if __name__ == "__main__":
    app()
