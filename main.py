from typing import Optional

from fastapi import FastAPI
from user import User
import os


app = FastAPI()



@app.get("/")
async def root():
    return {"message": "Hello World"}


@app.get("/users")
async def get_users():
    users = User.load()
    return users

"""@app.get("/items/{item_id}")
def read_item(item_id: int, q: Optional[str] = None):
    return {"item_id": item_id, "q": q}"""