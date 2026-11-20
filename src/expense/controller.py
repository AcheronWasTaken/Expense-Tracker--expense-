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
                form.reset()
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
                form.reset()
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
        error_message = ""

        choose_subscription = Form()
        choose_subscription.add_field("name", "Subscription Name", "str")

        choose_field = Form()
        choose_field.add_field("field_name", "What would you like to change?", "str", choices=["name", "expense"])

        name = ""
        while True:
            self.view.fill_form(choose_subscription, pre_message=error_message)

            if not choose_subscription.completed:
                raise FormNotCompleted

            name = choose_subscription.get("name")
            if not self.model.find_subscription(name): #type:ignore
                error_message = "A subscription with that name doesn't exist."
                choose_subscription.reset()
                continue
            break

        self.view.fill_form(choose_field)
        field = choose_field.get("field_name")

        if field == "expense":
            change_expense = Form()
            change_expense.add_field("duration", "Duration of the expense", "str", choices=["daily", "monthly", "yearly"])
            change_expense.add_field("expense", "Expense Amount", "float")

            self.view.fill_form(change_expense)

            duration = change_expense.get("duration")
            expense = change_expense.get("expense")

            self.model.update_subscription(name, "monthly_expense", expense, duration=duration) #type:ignore
            return

        if field == "name":
            change_name = Form()
            change_name.add_field("new_name", "New Name", "str")

            while True:
                self.view.fill_form(change_name, error_message)

                new_name = change_name.get("new_name")

                if self.model.find_subscription(new_name): #type:ignore
                    error_message = "A subscription with that name already exists."
                    change_name.reset()
                    continue

                self.model.update_subscription(name, field, new_name) #type:ignore
                break 


    def exit(self):
        raise Abort

    def run(self):
        while True:
            command = self.view.main()

            if not command in self.commands:
                continue

            self.commands[command]()

    

