from fastapi import APIRouter
from fastapi import (Request, 
                     HTTPException)

from core.conf.config import templates

from core.services.posts_service import post_service

templates_router = APIRouter()


@templates_router.get("/")
async def render_html(request: Request):
    """ Main types page. """
    
    return templates.TemplateResponse("index.html", {"request": request})


@templates_router.get("/type/{key}/")
async def render_html(request: Request, key: str):
    """ Get post with key. """

    post = post_service.get_post(key=key)

    if post:
        # TODO: Выпилить created из response

        return templates.TemplateResponse(
            "type.html",
            {"request": request,
             'post': post,
             'created': post.created.date()})
    else:
        return HTTPException(
            status_code=404
        )
