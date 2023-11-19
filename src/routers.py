from fastapi import APIRouter

from src.posts.router import posts_router
from src.comments.router import comments_router
from src.templates.router import templates_router


def get_api_routers() -> APIRouter:
    router = APIRouter(prefix="/api/v1", 
                       tags=["api"])
    
    router.include_router(posts_router, prefix="/post")
    router.include_router(comments_router, prefix="/comments")

    return router


def get_templates_router() -> APIRouter:
    router = APIRouter(include_in_schema=False)
    
    router.include_router(templates_router)
    
    return router