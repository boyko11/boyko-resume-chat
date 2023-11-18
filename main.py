import os

from fastapi import FastAPI
from routes.chat import chat_router
from fastapi.staticfiles import StaticFiles

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

app = FastAPI()

app.include_router(chat_router)

app.mount("/", StaticFiles(directory="frontend", html=True), name="static")
