from fastapi import APIRouter
from routes.templates import main


templates_router = APIRouter()
templates_router.include_router(main.router)