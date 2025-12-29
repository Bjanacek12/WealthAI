from contextlib import asynccontextmanager
from fastapi import FastAPI
from database import init_db

@asynccontextmanager
async def lifespan(app: FastAPI):
    print("WealthAI is starting up...")
    init_db()
    yield         # run until server stops
    print("WealthAI is shutting down...")

app = FastAPI(lifespan = lifespan)

@app.get("/")
def read_root():
    return {"message" : "WealthAI API is online"}

@app.get("/health")
def health_check():
    return{"status": "healthy", "database": "connected"}