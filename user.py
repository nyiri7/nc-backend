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
        users.append(user.__dict__)
        with open(filename, "w", encoding="utf-8") as f:
                try:
                    json.dump(users, f, indent=4)
                    return {"message": "Siker", "error": "Sikeres hozzáadás"}
                except json.JSONDecodeError:
                    return {"message": "Error saving user", "error": "Invalid JSON format"}
        
    @staticmethod
    def leave(inpUser, filename="user.json"):
        users = User.load()
        for u in users:
            if(u.get("id")==inpUser.id):
                u["amount"]=inpUser.amount
                with open(filename, "w", encoding="utf-8") as f:
                    try:
                        json.dump(users, f, indent=4)
                        return 1
                    except json.JSONDecodeError:
                        return 0
        

    @staticmethod
    def load(filename="user.json"):
        if not os.path.exists(filename):
            return []
        with open(filename, "r", encoding="utf-8") as f:
            try:
                return json.load(f)
            except json.JSONDecodeError:
                return []