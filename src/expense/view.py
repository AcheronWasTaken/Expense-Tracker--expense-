from .model import Model
from rich.layout import Layout
from rich.table import Table
from rich.text import Text
from rich.live import Live
from keyboard import read_event

class ModelInterface:
    def __init__(self, model:Model):
        self.model = model
        self.layout = self.build_layout()

    @staticmethod
    def build_table(headers:list, grid:bool=False):
        if grid:
            table = Table.grid()
        else:
            table = Table()

        for header in headers:
            table.add_column(header)

        return table

    def build_layout(self) -> Layout:
        if self.model.empty:
            return Layout("Wow...such empty!")

        model_table = self.build_table([
            "Name",
            "Expense ($)",
            "Score (%)"
        ])

        for subscription in self.model.get_table_values():
            name = subscription.name
            expense = Text(str(subscription.monthly_expense), style="cyan")

            if subscription.cost_score <= 50:
                score_color = "green"
            elif subscription.cost_score <= 75:
                score_color = "yellow"
            else:
                score_color = "red"

            score = Text(str(subscription.cost_score), style=score_color)

            model_table.add_row(name, expense, score)

        statistics_table = self.build_table(
            headers=["name", "value"],
            grid=True
        )

        for stat_name, stat_value in self.model.statistics.items():
            name = Text(stat_name, style="yellow")
            value = str(stat_value)

            statistics_table.add_row(name, value)

        layout = Layout()
        layout.split_row(
            Layout(model_table, name="model"),
            Layout(statistics_table, name="statistics")
        )
        return layout

    def view(self, update=False):
        if update:
            self.layout = self.build_layout()

        return self.layout
        

class CommandInterface:
    def __init__(self, commands:list[str]):
        self.commands = commands
        self.layout = self.build_layout(cursor=0)

    @staticmethod
    def build_table() -> Table:
        table = Table.grid()

        table.add_column("index")
        table.add_column("command")

        return table

    def build_layout(self, cursor:int):
        command_table = self.build_table()

        for index_value, command_value in enumerate(self.commands):
            index = Text(str(index_value))

            if cursor == index_value:
                command = Text(command_value, style="yellow")
            else:
                command = command_value

            command_table.add_row(index, command)

        return Layout(command_table, name="commands")

    def view(self, cursor:int=-1):
        if cursor != -1:
            self.layout = self.build_layout(cursor)

        return self.layout

class View:
    def __init__(self, model:Model, commands:list[str]):
        self.cursor_max = len(commands)
        self.commands = commands
        self.model_interface = ModelInterface(model)
        self.command_interface = CommandInterface(self.commands)

    def build_main(self, cursor:int):
        layout = Layout()
        layout.split_row(
            self.model_interface.view(),
            self.command_interface.view(cursor)
        )
        return layout

    def main(self) -> str:
        cursor = 0

        layout = self.build_main(cursor)

        with Live(layout, auto_refresh=False, transient=True) as live:
            while True:
                event = read_event(suppress=True)

                if event.event_type != "down":
                    continue

                key = event.name

                if key == "w":
                    cursor = self.shift_cursor_up(cursor)

                    layout["commands"].update(self.command_interface.view(cursor))
                    live.refresh()

                elif key == "s":
                    cursor = self.shift_cursor_down(cursor)

                    layout["commands"].update(self.command_interface.view(cursor))
                    live.refresh()
                elif key == "enter":
                    return self.commands[cursor]

    def shift_cursor_up(self, cursor:int):
        return self.cursor_max if cursor == 0 else cursor - 1
    
    def shift_cursor_down(self, cursor:int):
        return 0 if cursor == self.cursor_max else cursor + 1