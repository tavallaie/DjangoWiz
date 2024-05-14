# DjangoWiz

DjangoWiz is a simple and powerful toolkit to automate the generation of serializers, viewsets, URLs, and Docker configurations for your Django projects. This toolkit helps you quickly scaffold out necessary files based on your models, saving you time and effort.

## Features

- Automatically generates serializers, viewsets, and URLs based on your Django models.
- Supports generation of Dockerfile and Docker Compose configurations for development and production environments.
- Skips non-serializable classes and abstract models.
- Includes customizable templates using Jinja2.
- Provides flexible commands to generate different components individually or all together.

## Installation

1. **Install via pip:**
    ```bash
    pip install DjangoWiz
    ```

2. **Alternatively, clone the repository:**
    ```bash
    git clone https://github.com/yourusername/DjangoWiz.git
    cd DjangoWiz
    ```

3. **Install dependencies:**
    Ensure you have Python and Poetry installed, then run:
    ```bash
    poetry install
    ```

## Usage

### Generate All Files

Generate serializers, viewsets, routes, URLs, Dockerfile, and Docker Compose configurations:

```bash
djangowiz generate-files <your_app> <your_project> <path/to/models.py> --overwrite
```

### Generate Core Files Only

Generate serializers, viewsets, and routes without Docker-related files:

```bash
djangowiz generate_core_files <your_app> <your_project> <path/to/models.py> --overwrite
```

### Generate Individual Components

#### Generate Serializers

```bash
djangowiz generate_serializers <your_app> <your_project> <path/to/models.py> --overwrite
```

#### Generate Viewsets

```bash
djangowiz generate_viewsets <your_app> <your_project> <path/to/models.py> --overwrite
```

#### Generate URLs

```bash
djangowiz generate_urls <your_app> <your_project> <path/to/models.py> --overwrite
```

#### Generate Routes

```bash
djangowiz generate_routes <your_app> <your_project> <path/to/models.py> --overwrite
```

## Directory Structure

Ensure your project directory is structured as follows:

```
DjangoWiz/
├── DjangoWiz/
│   ├── __init__.py
│   ├── generate.py
│   ├── templates/
│       ├── docker-compose.dev.yml.j2
│       ├── docker-compose.prod.yml.j2
│       ├── Dockerfile.j2
│       ├── env.dev.j2
│       ├── env.prod.j2
│       ├── serializer.py.j2
│       ├── viewset.py.j2
│       ├── urls.py.j2
│       ├── routes.py.j2
├── pyproject.toml
├── README.md
├── LICENSE
```

## Customizing Templates

The templates used for generating files are located in the `DjangoWiz/templates` directory. You can customize these templates to fit your project's specific requirements. The templates use Jinja2 for rendering.

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for more details.

## Contributing

Contributions are welcome! Please open an issue or submit a pull request if you have any suggestions or improvements.

## Author

Ali Tavallaie - [a.tavallaie@gmail.com](mailto:a.tavallaie@gmail.com)

---

Happy coding!
