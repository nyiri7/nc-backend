from typing import Optional

from fastapi import FastAPI, Body
from fastapi.middleware.cors import CORSMiddleware
from user import User
import os



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



@app.get("/users")
async def get_users():
    users = User.load()
    return users



@app.post("/users")
async def add_user(data: dict = Body(...)):
    name = data.get("name")
    amount = data.get("amount")
    if not name or amount is None:
        return {"error": "Both 'name' and 'amount' are required."}
    user = User.create_and_save(name, amount)
    return {"message": "User added", "user": user}

"""@app.get("/items/{item_id}")
def read_item(item_id: int, q: Optional[str] = None):
    return {"item_id": item_id, "q": q}"""