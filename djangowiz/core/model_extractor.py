import ast
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
