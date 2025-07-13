import json
import os


class Log:
    
    def __init__(self, partyID, userID, msg):
        self.id = Log.getID()
        self.partyID = partyID
        self.userID = userID
        self.msg = msg
    
    @staticmethod
    def getID():
        if os.path.exists("log.json"):
            with open("log.json", "r", encoding="utf-8") as f:
                try:
                    logs = json.load(f)
                except json.JSONDecodeError:
                    logs = []
        else:
            logs = []
        if logs:
            return max(l.get("id", 0) for l in logs) + 1
        return 1
    
    @staticmethod
    def createSave(partyID,userID,msg):
        l= Log(partyID,userID,msg)
        if os.path.exists("log.json"):
            with open("log.json", "r", encoding="utf-8") as f:
                try:
                    logs = json.load(f)
                except json.JSONDecodeError:
                    logs = []
                logs.append(l)
                json.dump(logs, f, indent=4)
        else:
            logs = []
    
    @staticmethod
    def load(id):
        if os.path.exists("log.json"):
            with open("log.json", "r", encoding="utf-8") as f:
                try:
                    logs = json.load(f)
                except json.JSONDecodeError:
                    logs = []
        else:
            logs=[]
        
        if id is None:
            return logs
        else:
            res = []
            for log in logs:
                if log.id==id:
                    res.append(log)
            return res