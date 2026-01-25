import uuid
from dataclasses import dataclass, field
from datetime import datetime
from typing import List, Optional

@dataclass
class User:
    name: str
    image: str
    money: float
    id: str = field(default_factory=lambda: str(uuid.uuid4()))
    current_party_id: Optional[str] = None

@dataclass
class Party:
    # Fontos: a mutable típusoknál (mint a list) field(default_factory=...) kell
    user_ids: List[str] = field(default_factory=list)
    id: str = field(default_factory=lambda: str(uuid.uuid4()))
    start_time: datetime = field(default_factory=datetime.now)
    end_time: Optional[datetime] = None
    adminCode:str

@dataclass
class MoneyLog:
    user_id: str
    action: str
    amount_change: float
    id: str = field(default_factory=lambda: str(uuid.uuid4()))
    timestamp: datetime = field(default_factory=datetime.now)
    party_id: Optional[str] = None

@dataclass
class PartySummary:
    party: Party