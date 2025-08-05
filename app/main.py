from fastapi import FastAPI
from app.api import app as app_router
from app.api import chat as chat_router
from app.api import agent_config as agent_config_router
from app.api import tool_config as tool_config_router

app = FastAPI()

app.include_router(app_router.router)
app.include_router(chat_router.router)
app.include_router(agent_config_router.router)
app.include_router(tool_config_router.router)

# To run: uvicorn app.main:app --reload