import uuid
from dataclasses import dataclass, field
from datetime import datetime
from typing import List, Optional
from pydantic import BaseModel

class User(BaseModel):
    name: str
    image: str
    money: float
    id: str = field(default_factory=lambda: str(uuid.uuid4()))
    current_party_id: Optional[str] = None


class Party(BaseModel):
    id: str = field(default_factory=lambda: str(uuid.uuid4()))
    adminCode: str = ""
    start_time: datetime = field(default_factory=datetime.now)
    end_time: Optional[datetime] = None



class MoneyLog(BaseModel):
    user_id: str
    action: str
    amount_change: float
    id: str = field(default_factory=lambda: str(uuid.uuid4()))
    timestamp: datetime = field(default_factory=datetime.now)
    party_id: Optional[str] = None


class PartySummary(BaseModel):
    party: Party