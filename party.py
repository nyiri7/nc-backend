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
                    return j["id"]+1
                except json.JSONDecodeError:
                    return 1
        else:
            return 1
    
    @staticmethod
    def load(id):
        if os.path.exists("party.json"):
            with open("party.json", "r", encoding="utf-8") as f:
                try:
                    j = json.load(f)
                    for p in j["parties"]:
                        if p["id"]== id:
                            return p
                    return j
                except json.JSONDecodeError:
                    return {"message": "No parties found."}
        else:
            return 1

    @staticmethod
    def removeUser(pID,uID):
        parties = Party.load()
        index = -1
        for p in parties["parties"]:
            if p["id"]== pID:
                for i,u in enumerate(p["users"]):
                    if u["id"] == uID:
                        index = i
                if index != -1:
                    del p["users"][index]
        return {"message": "User removed from party."} if index != -1 else {"message": "User not found in party."}



    @staticmethod
    def createParty(party):
        if os.path.exists("party.json"):
            with open("party.json", "r", encoding="utf-8") as f:
                try:
                    j= json.load(f)
                    j["id"] +=1
                    j["parties"].append(party.to_dict())
                except Exception as e:
                    return {"message": "Error creating party1", "error": str(e)}
            with open("party.json", "w", encoding="utf-8") as k:
                try:
                    json.dump(j, k, indent=4)
                    return {"id":j["id"]}
                except Exception as e:
                    return {"message": "Error creating party", "error": str(e)}
        else:
            j = {"id": 1, "parties": [party.to_dict()]}
            with open("party.json", "w", encoding="utf-8") as f:
                try:
                    json.dump(j, f, indent=4)
                except Exception as e:
                    return {"message": "Error creating party", "error": str(e)}
            return {"id": 1}
    
    def addMember(self, user):
        if os.path.exists("party.json"):
            with open("party.json", "r", encoding="utf-8") as f:
                try:
                    j = json.load(f)
                except json.JSONDecodeError:
                    return False
            j.parties[self.id - 1]['users'].append(user)
            with open("party.json", "w", encoding="utf-8") as f:
                json.dump(j, f, indent=4)
            return True
        else:
            j = {'id': 1, 'parties': [{'users': [user]}]}
            with open("party.json", "w", encoding="utf-8") as f:
                json.dump(j, f, indent=4)
            return True
        
    def to_dict(self):
        if self.end != "":
            return {
                "id": self.id,
                "start": self.start.isoformat(),
                "end": self.end.isoformat(),
                "users": self.users
            }
        return {
            "id": self.id,
            "start": self.start.isoformat(),
            "end": "",
            "users": self.users
        }