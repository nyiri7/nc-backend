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
        
    @staticmethod
    def createParty(party):
        if os.path.exists("party.json"):
            with open("party.json", "r", encoding="utf-8") as f:
                try:
                    j = json.load(f)
                    
                except json.JSONDecodeError:
                    return False
                j.id +=1
                j.parties.append(party)
                json.dump(j, f, indent=4)
                return True
        else:
            j = {'id': 1, 'parties': [party]}
            with open("party.json", "w", encoding="utf-8") as f:
                json.dump(j, f, indent=4)
            return True
    
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