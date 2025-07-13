import json
import os


class User:
    def __init__(self, id, name, amount):
        self.id = id
        self.name = name
        self.amount = amount

    @staticmethod
    def create_and_save(name, amount, filename="user.json"):
        if os.path.exists(filename):
            with open(filename, "r", encoding="utf-8") as f:
                try:
                    users = json.load(f)
                except json.JSONDecodeError:
                    users = []
        else:
            users = []
        if users:
            new_id = max(u.get("id", 0) for u in users) + 1
        else:
            new_id = 1
        user = User(new_id, name, amount)
        user.save(filename)
        return {"id": new_id, "name": name, "amount": amount}

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