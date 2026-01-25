import json
import os
from dataclasses import asdict
from typing import List, Optional

# Új importok a biztonsághoz
from fastapi import FastAPI, HTTPException, Body, Header, Depends
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse, HTMLResponse
from passlib.context import CryptContext

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
    
    # --- JAVÍTÁS: Hossz ellenőrzése a hiba elkerülése érdekében ---
    # A bcrypt max 72 byte-ot bír el. Ha ennél hosszabb a kapott kód,
    # akkor az biztosan nem a helyes jelszó, és hibát okozna a verify() hívása.
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

# PÉLDA: Egy védett végpont, amit csak a kód birtokában lehet hívni
@app.get("/secret-data", dependencies=[Depends(verify_admin_code)])
async def get_secret_data():
    return {"secret": "Itt vannak a titkos adatok, mert jó kódot küldtél!"}

# Ha azt szeretnéd, hogy MINDEN végpont védett legyen, 
# akkor az app definíciónál is megadhatod:
# app = FastAPI(dependencies=[Depends(verify_admin_code)])