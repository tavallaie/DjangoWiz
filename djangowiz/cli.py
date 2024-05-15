import typer
from djangowiz.core import ModelExtractor, ProjectGenerator

app = typer.Typer()


@app.command()
def generate_files(
    app_name: str,
    project_name: str,
    model_file: str,
    single_file: bool = False,
    overwrite: bool = False,
    template_dir: str = None,
):
    model_names = ModelExtractor.extract_model_names(model_file)
    generator = ProjectGenerator(app_name, project_name, model_names, template_dir)
    generator.generate_all(single_file, overwrite)
    print(
        f"Files for {len(model_names)} models have been generated in the {app_name} directory."
    )


@app.command()
def generate_core_files(
    app_name: str,
    project_name: str,
    model_file: str,
    single_file: bool = False,
    overwrite: bool = False,
    template_dir: str = None,
):
    model_names = ModelExtractor.extract_model_names(model_file)
    generator = ProjectGenerator(app_name, project_name, model_names, template_dir)
    generator.generate_core_files(single_file, overwrite)
    print(
        f"Serializers, viewsets, and routes for {len(model_names)} models have been generated in the {app_name} directory."
    )


@app.command()
def generate_serializers(
    app_name: str,
    project_name: str,
    model_file: str,
    single_file: bool = False,
    overwrite: bool = False,
    template_dir: str = None,
):
    model_names = ModelExtractor.extract_model_names(model_file)
    generator = ProjectGenerator(app_name, project_name, model_names, template_dir)
    generator.generate_serializers(single_file, overwrite)
    print(
        f"Serializers for {len(model_names)} models have been generated in the {app_name} directory."
    )


@app.command()
def generate_viewsets(
    app_name: str,
    project_name: str,
    model_file: str,
    single_file: bool = False,
    overwrite: bool = False,
    template_dir: str = None,
):
    model_names = ModelExtractor.extract_model_names(model_file)
    generator = ProjectGenerator(app_name, project_name, model_names, template_dir)
    generator.generate_viewsets(single_file, overwrite)
    print(
        f"Viewsets for {len(model_names)} models have been generated in the {app_name} directory."
    )


@app.command()
def generate_urls(
    app_name: str,
    project_name: str,
    model_file: str,
    overwrite: bool = False,
    template_dir: str = None,
):
    model_names = ModelExtractor.extract_model_names(model_file)
    generator = ProjectGenerator(app_name, project_name, model_names, template_dir)
    generator.generate_urls(overwrite)
    print(f"URLs have been generated in the {app_name} directory.")


@app.command()
def generate_routes(
    app_name: str,
    project_name: str,
    model_file: str,
    overwrite: bool = False,
    template_dir: str = None,
):
    model_names = ModelExtractor.extract_model_names(model_file)
    generator = ProjectGenerator(app_name, project_name, model_names, template_dir)
    generator.generate_routes(overwrite)
    print(f"Routes have been generated in the {app_name} directory.")


if __name__ == "__main__":
    app()
