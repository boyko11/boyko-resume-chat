import os

from fastapi import FastAPI
from routes.chat import chat_router
from fastapi.staticfiles import StaticFiles

from routes.config import config_router

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

app = FastAPI()

app.include_router(chat_router)
app.include_router(config_router)

app.mount("/", StaticFiles(directory="frontend", html=True), name="static")
