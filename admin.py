import json
import os


class Admin:
    def __init__(self,pin,name):
        self.pin = pin
        self.name = name
    
    @staticmethod
    def getAdmin(id: int = 0):
        if os.path.exists("admin.json"):
            with open("admin.json", "r", encoding="utf-8") as f:
                try:
                    j = json.load(f)
                    return j
                except json.JSONDecodeError:
                    return {"message": "No admin found."}
            for admin in j["admins"]:
                if admin["pin"] == id:
                    return True
        else:
            return {"message": "No admin file found."}