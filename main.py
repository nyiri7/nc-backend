from typing import List, Optional
from fastapi import FastAPI, HTTPException, Body, Header, Depends
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse, HTMLResponse, Response
from passlib.context import CryptContext
import uuid
from models import User, Party
from data_layer import JsonDB
import os
from mangum import Mangum



VALID_ADMIN_HASHES = [h.strip() for h in os.getenv("VALID_ADMIN_HASHES", "").split(",") if h.strip()]
print("Valid admin hashes loaded:", VALID_ADMIN_HASHES)


# --- Adattároló réteg ---
db = JsonDB()

# --- API App ---
app = FastAPI()
handler = Mangum(app)

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
            if x_admin_code == stored_hash:
                is_valid = True
                break
        except Exception as e:
            print("Skipping invalid hash entry:", stored_hash, "->", e)
            continue

    if not is_valid:
        raise HTTPException(status_code=403, detail="Érvénytelen admin kód.")
    
    return True

# --- Endpointok ---

@app.get("/")
async def root():
    return {"message": "Party API Running"}


@app.get("/code", dependencies=[Depends(verify_admin_code)])
async def code(x_admin_code: Optional[str] = Header(None)):
    response = Response()
    response.headers["X-Code"] = x_admin_code
    response.headers["X-Expiration"] = "3600"
    response.set_cookie(key="admin_code", value=x_admin_code, max_age=3600, httponly=True, secure=True)
    return response

@app.get("/mate")
async def mate():
    return FileResponse("images/mate.png", media_type="image/png")

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

@app.post("/api/user", dependencies=[Depends(verify_admin_code)])
async def create_User(user:User):
    user.id = str(uuid.uuid4())
    db.save_user(user)
    return user

@app.put("/api/user", dependencies=[Depends(verify_admin_code)])
async def update_User(user:User):
    db.update_user(user)
    return {"message": "User updated successfully", "user": user}

@app.delete("/api/user", dependencies=[Depends(verify_admin_code)])
async def delete_User(user:User):
    db.delete_user(user)
    return {"message": "User deleted successfully"}

#Party Endpoints
@app.get("/api/party")
async def get_Party(x_admin_code: Optional[str] = Header(None)):
    partys = db.get_parties()
    if x_admin_code:
        for p in partys:
            if p["adminCode"] == x_admin_code:
                return p
    return {"message": "No party found with the provided admin code."}

@app.post("/api/party", dependencies=[Depends(verify_admin_code)])
async def create_Party(party:Party,x_admin_code: Optional[str] = Header(None)):
    party.id = str(uuid.uuid4())
    party.adminCode = x_admin_code
    party.start_time = int(uuid.uuid1().time)
    db.save_party(party)
    return party

@app.put("/api/AddParty", dependencies=[Depends(verify_admin_code)])
async def update_Party(party:Party,user:User):
    db.update_party(party)
    user.current_party_id = party.id
    db.update_user(user)
    return {"message": "Party updated successfully", "party": party}

@app.put("/api/RemoveParty", dependencies=[Depends(verify_admin_code)])
async def update_Party(party:Party,user:User):
    db.update_party(party)
    user.current_party_id = ""
    db.update_user(user)
    return {"message": "Party updated successfully", "party": party}

@app.delete("/api/party", dependencies=[Depends(verify_admin_code)])
async def delete_Party(party:Party):
    users = db.get_users()
    for u in users:
        if u.current_party_id == party.id:
            return {"message": "Party contains people."}
    db.delete_party(party)
    return {"message": "Party deleted successfully"}