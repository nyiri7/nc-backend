import json
import os


class Party:
    def __init__(self,start,end,users):
        self.id = Party.getID()
        self.users = users
        self.start = start
        self.end = end

    
    @staticmethod
    def getID():
        if os.path.exists("party.json"):
            with open("party.json", "r", encoding="utf-8") as f:
                try:
                    j = json.load(f)
                    return j.id
                except json.JSONDecodeError:
                    return 1
        else:
            return 1
        
    def createParty():
        if os.path.exists("party.json"):
            with open("party.json", "r", encoding="utf-8") as f:
                try:
                    j = json.load(f)
                except json.JSONDecodeError:
                    return "JSON error"
        else:
            return 1