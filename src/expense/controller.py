from pathlib import Path
from.view import View
from .model import Model
from click import Abort

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
        pass

    def remove_subscription(self):
        pass

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

    

