from fastapi import APIRouter
from routes.api.v1 import posts

api_router = APIRouter()
api_router.include_router(posts.router, prefix='/v1')
