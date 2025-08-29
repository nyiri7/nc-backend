from datetime import datetime

from fastapi import FastAPI, Body
from fastapi.middleware.cors import CORSMiddleware
from party import Party
from user import User



app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)



@app.get("/")
async def root():
    return {"message": "Hello World"}



@app.get("/userss")
async def get_users():
    users = User.load()
    return users


@app.get("/parties")
async def get_parties(id: int = 0):
    result = Party.load(id)
    return result

@app.post("/parties")
async def add_party(data:dict = Body(...)):
    r = Party.createParty(Party(datetime.now(),"",data.get("users", [])))
    return r

@app.put("/parties")
async def leaveParty(data: dict = Body(...)):
    m = data.get("user")
    User.leave(User(m.get("id"), m.get("name"), m.get("amount")))
    return Party.removeUser(data.get("partyID"), m.get("id"))
    

@app.post("/users")
async def add_user(data: dict = Body(...)):
    user = User.create_and_save(data.get("name"), data.get("amount"))
    return user
