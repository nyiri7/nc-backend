from typing import List, Optional

# Új importok a biztonsághoz
from fastapi import FastAPI, HTTPException, Body, Header, Depends
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse, HTMLResponse
from passlib.context import CryptContext
import uuid

# Dataclassok importálása (Feltételezem ezek léteznek a models.py-ban)
from models import User, Party, MoneyLog
from data_layer import JsonDB


pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


VALID_ADMIN_HASHES = [

]


# --- Adattároló réteg ---
db = JsonDB()

# --- API App ---
app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


async def verify_admin_code(x_admin_code: Optional[str] = Header(None)):
    if x_admin_code is None:
        raise HTTPException(status_code=401, detail="Nincs megadva admin kód (X-Admin-Code header hiányzik).")
    if len(x_admin_code.encode('utf-8')) > 72:
        raise HTTPException(status_code=403, detail="Érvénytelen admin kód (túl hosszú).")

    is_valid = False
    for stored_hash in VALID_ADMIN_HASHES:
        try:
            if pwd_context.verify(x_admin_code, stored_hash):
                is_valid = True
                break
        except Exception:
            continue

    if not is_valid:
        raise HTTPException(status_code=403, detail="Érvénytelen admin kód.")
    
    return True

# --- Endpointok ---

@app.get("/")
async def root():
    return {"message": "Party API Running"}

@app.get("/pin")
async def get_pin():
    return HTMLResponse(content=open("pin.html").read(), status_code=200)


@app.get("/secret-data", dependencies=[Depends(verify_admin_code)])
async def get_secret_data():
    return {"secret": "Itt vannak a titkos adatok, mert jó kódot küldtél!"}

#User Endpoints
@app.get("/api/users")
async def get_Users():
    return db.get_users()

@app.post("/api/user")
async def create_User(user:User):
    user.id = str(uuid.uuid4())
    db.save_user(user)
    return {"message": "User created successfully", "user_id": user.id}

@app.put("/api/user")
async def update_User(user:User):
    db.update_user(user)
    return {"message": "User updated successfully", "user": user}

@app.delete("/api/user")
async def delete_User(user:User):
    db.delete_user(user)
    return {"message": "User deleted successfully"}

#Party Endpoints
@app.get("/api/partys")
async def get_Partys():
    return db.get_parties()

@app.post("/api/party")
async def create_Party(party:Party):
    party.id = str(uuid.uuid4())
    db.save_party(party)
    return {"message": "Party created successfully", "party_id": party.id}

@app.put("/api/AddParty")
async def update_Party(party:Party,user:User):
    db.update_party(party)
    user.current_party_id = party.id
    db.update_user(user)
    return {"message": "Party updated successfully", "party": party}

@app.put("/api/RemoveParty")
async def update_Party(party:Party,user:User):
    db.update_party(party)
    user.current_party_id = ""
    db.update_user(user)
    return {"message": "Party updated successfully", "party": party}

@app.delete("/api/party")
async def delete_Party(party:Party):
    db.delete_party(party)
    return {"message": "Party deleted successfully"}