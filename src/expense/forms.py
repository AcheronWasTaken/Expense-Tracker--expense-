from rich.prompt import Prompt, FloatPrompt, Confirm
from rich.console import Console

class FormNotCompleted(Exception):
    pass

class Field:
    def __init__(self, name:str, prompt:str, field_type:str, choices:list):
        type_index = {"str": Prompt, "float": FloatPrompt, "confirm": Confirm}

        self.name = name
        self.prompt = prompt
        self.field_type = type_index[field_type]
        self.choices = choices
        self.answer = None

    def fill_answer(self, console:Console):
        if self.choices:
            self.answer = self.field_type.ask(self.prompt, choices=self.choices, case_sensitive=False, console=console)
        else:
            self.answer = self.field_type.ask(self.prompt, console=console)

class Form:
    def __init__(self):
        self.fields:dict[str, Field] = {}
        self.completed = False
        self.answered = 0

    def add_field(self, field_name:str, prompt:str, field_type:str, choices:list=[]):
        self.fields.update({field_name: Field(field_name, prompt, field_type, choices)})

    def get(self, field_name:str):
        return self.fields[field_name].answer

    def get_fields(self):
        return self.fields.keys()

    def ask(self, field_name:str, console:Console):
        self.fields[field_name].fill_answer(console=console)

        self.answered += 1
        if self.answered == len(self.fields):
            self.completed = True

    def reset(self):
        for field in self.fields.values():
            field.answer = None

        self.answered = 0
        self.completed = False
    
        
