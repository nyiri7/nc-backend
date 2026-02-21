import json
import os
from dataclasses import asdict
from typing import List

from models import User, Party


class JsonDB:
    def __init__(self):
        self.files = {
            "users": "users.json",
            "parties": "parties.json",
            "logs": "logs.json"
        }
        self._init_files()

    def _init_files(self):
        for file in self.files.values():
            if not os.path.exists(file):
                with open(file, 'w', encoding='utf-8') as f:
                    json.dump([], f)

    def _read_json(self, key):
        with open(self.files[key], 'r', encoding='utf-8') as f:
            return json.load(f)

    def _write_json(self, key, data):
        with open(self.files[key], 'w', encoding='utf-8') as f:
            # A datetime és dataclass kezeléséhez a default=str segít
            json.dump(data, f, indent=4, default=str)

    # --- User műveletek ---
    def get_users(self) -> List[dict]:
        return self._read_json("users")

    def save_user(self, user: User):
        users = self.get_users()
        users.append(user.__dict__)
        self._write_json("users", users)

    def update_user(self, updated_user: User):
        users = self.get_users()
        users = [u if u['id'] != updated_user.id else updated_user.__dict__ for u in users]
        self._write_json("users", users)

    def delete_user(self, user: User):
        users = self.get_users()
        users = [u for u in users if u['id'] != user.id]
        self._write_json("users", users)
        
    def get_user_by_id(self, user_id: str):
        users = self.get_users()
        for u in users:
            if u['id'] == user_id:
                return u
        return None

    # --- Party műveletek ---
    def get_parties(self) -> List[dict]:
        return self._read_json("parties")

    def save_party(self, party: Party):
        parties = self.get_parties()
        parties.append(party.__dict__)
        self._write_json("parties", parties)

    def update_party(self, updated_party: dict):
        parties = self.get_parties()
        parties = [p if p['id'] != updated_party['id'] else updated_party.__dict__ for p in parties]
        self._write_json("parties", parties)

    def get_party_by_id(self, party_id: str):
        parties = self.get_parties()
        for p in parties:
            if p['id'] == party_id:
                return p
        return None
