import os
from djangowiz.core.io_handler import IOHandler


class ProjectIOHandler:
    def __init__(
        self,
        config_file: str,
        default_config_file: str,
        template_dir: str,
        default_template_dir: str,
        generator_dir: str,
    ):
        self.config_file = config_file
        self.default_config_file = default_config_file
        self.template_dir = template_dir
        self.default_template_dir = default_template_dir
        self.generator_dir = generator_dir

    def export_config(self, export_path: str):
        """Export combined generators.yaml, templates, and generators to a specified directory."""
        os.makedirs(export_path, exist_ok=True)

        # Combine user and default configurations
        user_config = IOHandler.load_yaml(self.config_file)
        default_config = IOHandler.load_yaml(self.default_config_file)
        combined_config = {"generators": {}}

        for name, generator_config in default_config.get("generators", {}).items():
            combined_config["generators"][name] = generator_config

        for name, generator_config in user_config.get("generators", {}).items():
            if name in combined_config["generators"]:
                combined_config["generators"][name]["options"].update(
                    generator_config.get("options", {})
                )
            else:
                combined_config["generators"][name] = generator_config

        # Export combined generators.yaml
        IOHandler.save_yaml(
            combined_config, os.path.join(export_path, "generators.yaml")
        )

        print(f"Combined generators.yaml exported to {export_path}.")

        # Copy user templates
        IOHandler.copy_tree(self.template_dir, os.path.join(export_path, "templates"))

        # Copy default templates that are missing in user templates
        for root, dirs, files in os.walk(self.default_template_dir):
            for file in files:
                rel_path = os.path.relpath(
                    os.path.join(root, file), self.default_template_dir
                )
                dst_path = os.path.join(export_path, "templates", rel_path)
                if not os.path.exists(dst_path):
                    IOHandler.copy_file(os.path.join(root, file), dst_path)

        print(f"Templates exported to {export_path}.")

        # Copy user generators
        IOHandler.copy_tree(self.generator_dir, os.path.join(export_path, "generators"))

        # Copy default generators that are missing in user generators
        default_generators_dir = os.path.join(
            os.path.dirname(__file__), "..", "repo", "generators"
        )
        for root, dirs, files in os.walk(default_generators_dir):
            for file in files:
                rel_path = os.path.relpath(
                    os.path.join(root, file), default_generators_dir
                )
                dst_path = os.path.join(export_path, "generators", rel_path)
                if not os.path.exists(dst_path):
                    IOHandler.copy_file(os.path.join(root, file), dst_path)

        print(f"Generators exported to {export_path}.")

    def import_config(self, import_path: str):
        """Import generators.yaml, templates, and generators from a specified directory."""
        IOHandler.copy_file(
            os.path.join(import_path, "generators.yaml"), self.config_file
        )
        IOHandler.copy_tree(os.path.join(import_path, "templates"), self.template_dir)
        IOHandler.copy_tree(os.path.join(import_path, "generators"), self.generator_dir)
        print(f"Configuration, templates, and generators imported from {import_path}.")
