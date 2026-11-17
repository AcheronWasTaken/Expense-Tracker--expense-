from pathlib import Path
import json
from typing import Literal
import statistics as stat

class SubscriptionExists(Exception):
    pass

class SubscriptionNotFound(Exception):
    pass

class Subscription:
    def __init__(self, name:str, monthly_expense:float):
        self.name = name
        self.monthly_expense = monthly_expense
        self.cost_score = -1

    def get_raw(self):
        return {
            "name": self.name,
            "monthly_expense": self.monthly_expense
        }

    def set(self, key:str, value:float|str):
        if not key in self.__dict__:
            raise KeyError(f"Key ({key}) doesn't exist as a valid member of class Subscription")

        self.__setattr__(key, value)

class Model:
    def __init__(self, file_path:Path):
        self.file_path = file_path
        self.data = self.read_data(file_path)
        self.index = self.make_index(self.data)
        self.empty = not bool(self.data)
        self.statistics = self.make_statistics()
        self.assign_scores()

    def assign_scores(self):
        total = self.statistics["total"]

        for subscription in self.data.values():
            score = (1 - (total - subscription.monthly_expense)/total) * 100

            subscription.set("cost_score", round(score, 3))

    def make_statistics(self) -> dict[str, float]:
        if self.empty:
            return {}

        buffer = {}

        expenses = [subscription.monthly_expense for subscription in self.data.values()]

        total = sum(expenses)
        mean = round(stat.mean(expenses),3)
        standard_deviation = round(stat.stdev(expenses), 3) if len(self.data) > 2 else 0
        minimum = min(expenses)
        maximum = max(expenses)

        buffer.update({
            "total": total,
            "mean": mean,
            "standard deviation": standard_deviation,
            "minimum": minimum,
            "maximum": maximum
        })

        return buffer

    def get_table_values(self):
        return self.data.values()

    def add_subscription(self, name:str, expense:float, duration:Literal["daily", "monthly", "yearly"]):
        if name in self.index:
            raise SubscriptionExists(f"Subscription with name ({name}) already exists")

        monthly_expense = self.format_expense(expense, duration)
        subscription = Subscription(name, monthly_expense)
        hash_value = hash(subscription)

        self.data.update({hash_value: subscription})
        self.index.update({subscription.name: hash_value})

        self.empty = False

    def remove_subscription(self, name:str):
        if not name in self.index:
            raise SubscriptionNotFound(f"No subscription with name {name} exists")

        del self.data[self.index[name]]

    def update_subscription(self, name:str, key:str, value:str|float):
        if not name in self.index:
            raise SubscriptionNotFound(f"No subscription with name {name} exists")

        subscription = self.data[self.index[name]]
        subscription.set(key, value)

        if key == "name" and isinstance(value, str):
            self.index[value] = self.index.pop(name)

    @staticmethod
    def make_index(data:dict[int, Subscription]) -> dict[str, int]:
        buffer = {}
        for hash, subscription in data.items():
            buffer.update({hash:subscription.name})

        return buffer

    @staticmethod
    def format_expense(expense:float, duration:Literal["daily", "monthly", "yearly"]):
        if duration == "daily":
            return expense * 365 / 12
        
        if duration == "yearly":
            return expense / 12

        return expense

    @staticmethod
    def read_data(file_path:Path) -> dict[int, Subscription]:
        if not file_path.exists():
            return {}

        data:dict[int, Subscription] = {}

        buffer:list[dict] = []
        with open(file_path, "r") as file:
            buffer = json.load(file)

        for dict in buffer:
            subscription = Subscription(
                dict["name"],
                dict["monthly_expense"]
            )

            data.update({hash(subscription):subscription})

        return data

    @staticmethod
    def write_data(file_path:Path, data:dict[int, Subscription]):
        buffer = []

        for subscription in data.values():
            buffer.append(subscription.get_raw())

        with open(file_path, "w") as file:
            json.dump(buffer, file)     

   


        