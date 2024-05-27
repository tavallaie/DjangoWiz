# djangowiz/repo/generators/test_generator.py

from djangowiz.core.base_generator import BaseGenerator
import os
import re


class TestGenerator(BaseGenerator):
    def generate(self, overwrite: bool = False, template: str = None, **kwargs):
        if "single" in template:
            self.generate_single_file(overwrite, template)
        else:
            self.generate_multi_file(overwrite, template)

    def generate_single_file(self, overwrite: bool, template: str):
        fixtures = {
            model_name: self.get_fixtures(model_name) for model_name in self.model_names
        }
        context = {
            "app_name": self.app_name,
            "model_names": self.model_names,
            "fixtures": fixtures,
        }
        content = self.render_template(template, context)
        file_path = os.path.join(self.app_name, "tests", "test_api.py")
        self.write_file(file_path, content, overwrite)

    def generate_multi_file(self, overwrite: bool, template: str):
        fixtures = self.get_fixtures()
        for model_name in self.model_names:
            context = {
                "app_name": self.app_name,
                "model_name": model_name,
                "fixtures": fixtures.get(model_name, []),
            }
            content = self.render_template(template, context)
            file_path = os.path.join(
                self.app_name, "tests", f"test_{model_name.lower()}.py"
            )
            self.write_file(file_path, content, overwrite)

    def get_fixtures(self, model_name):
        fixtures_dir = os.path.join(os.path.dirname(self.model_file), "fixtures")
        for root, _, files in os.walk(fixtures_dir):
            for file in files:
                if re.match(rf"^\d+_{model_name.lower()}_seeding\.json$", file):
                    return os.path.relpath(
                        os.path.join(root, file), start=os.path.dirname(self.model_file)
                    )
        return f"{model_name.lower()}_fixtures.json"  # Fallback fixture file name
