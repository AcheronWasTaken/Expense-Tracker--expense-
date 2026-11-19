from pathlib import Path
from.view import View
from .model import Model
from click import Abort
from .forms import Form, FormNotCompleted

class Controller:
    def __init__(self, file_path:Path):
        self.commands = {
            "Add Subscription": self.add_subscription,
            "Remove Subscription": self.remove_subscription,
            "Update Subscription": self.update_subscription,
            "Exit": self.exit
        }

        self.model = Model(file_path)
        self.view = View(self.model, list(self.commands.keys()))

    def add_subscription(self):
        error_message = ""
        name = ""

        form = Form()
        form.add_field("name", "Subscription Name", "str")

        while True:
            self.view.fill_form(form, pre_message=error_message)

            if not form.completed:
                raise FormNotCompleted

            name = form.get("name")
            if self.model.find_subscription(name): #type:ignore
                error_message = "A subscription with that name already exists."
                continue
            break

        error_message = ""
        form = Form()
        form.add_field("duration", "Duration of the expense", "str", choices=["daily", "monthly", "yearly"])
        form.add_field("expense", "Expense Amount", "float")

        self.view.fill_form(form, pre_message=error_message)

        if not form.completed:
            raise FormNotCompleted

        duration = form.get("duration")
        expense = form.get("expense")

        self.model.add_subscription(name, expense, duration) #type:ignore

    def remove_subscription(self):
        error_message = ""
        form = Form()
        form.add_field("name", "Subscription name", "str")

        while True:
            self.view.fill_form(form, pre_message=error_message)

            if not form.completed:
                raise FormNotCompleted

            if not self.model.find_subscription(form.get("name")): #type:ignore
                error_message = "Could not find a subscription with the name"
                continue
            break

        confirm_form = Form()
        confirm_form.add_field("confirm", "Are you sure?", "confirm")
 
        self.view.fill_form(confirm_form)

        if not confirm_form.completed:
            raise FormNotCompleted

        if not confirm_form.get("confirm"):
            return

        self.model.remove_subscription(form.get("name")) #type:ignore

    def update_subscription(self):
        pass

    def exit(self):
        raise Abort

    def run(self):
        while True:
            command = self.view.main()

            if not command in self.commands:
                continue

            self.commands[command]()

    

