import json
import os

class User:
    def __init__(self, id, name, amount):
        self.id = id
        self.name = name
        self.amount = amount

    def save(self, filename="user.json"):
        data = {"id": self.id, "name": self.name, "amount": self.amount}
        if os.path.exists(filename):
            with open(filename, "r", encoding="utf-8") as f:
                try:
                    users = json.load(f)
                except json.JSONDecodeError:
                    users = []
        else:
            users = []
        updated = False
        for i, g in enumerate(users):
            if g.get("id") == self.id:
                users[i] = data
                updated = True
                break
        if not updated:
            users.append(data)

        with open(filename, "w", encoding="utf-8") as f:
            json.dump(users, f, indent=4)
    
    @staticmethod
    def load(filename="user.json"):
        if not os.path.exists(filename):
            return []
        with open(filename, "r", encoding="utf-8") as f:
            try:
                return json.load(f)
            except json.JSONDecodeError:
                return []