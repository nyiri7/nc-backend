import json
import os
from dataclasses import asdict
from typing import List

from fastapi import FastAPI, HTTPException, Body
from fastapi.middleware.cors import CORSMiddleware

# Dataclassok importálása
from models import User, Party, MoneyLog

from data_layer import JsonDB

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

@app.get("/")
async def root():
    return {"message": "Party API Running (No Pydantic)"}


