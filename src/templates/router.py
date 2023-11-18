from fastapi import APIRouter
from fastapi import (Request, 
                     HTTPException)

from core.conf.config import templates

from core.services.posts_service import post_service

templates_router = APIRouter()


@templates_router.get("/")
async def render_html(request: Request):
    """ Create types page. """
    
    return templates.TemplateResponse("create.html", {"request": request})


@templates_router.get("/type/{key}/")
async def render_html(request: Request, key: str):
    """ Get post with key. """

    post = post_service.get_post(key=key)

    if post:
        return templates.TemplateResponse(
            "type.html",
            {"request": request,
             'post': post,
             'created': post.created.date()})
    else:
        return HTTPException(
            status_code=404
        )
