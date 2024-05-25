from djangowiz.core.base_generator import BaseGenerator


class ViewsetGenerator(BaseGenerator):
    def generate(self, overwrite: bool = False, template: str = None, **kwargs):
        template = self.env.get_template(template)
        for model_name in self.model_names:
            content = template.render(app_name=self.app_name, model_name=model_name)
            file_path = f"{self.app_name}/viewsets/{model_name.lower()}.py"
            self.write_file(file_path, content, overwrite)
