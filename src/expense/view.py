from .model import Model
from rich.layout import Layout

class ModelInterface:
    def __init__(self, model:Model):
        self.model = model

    def build_layout(self) -> Layout:
        