from fastapi import APIRouter
from fastapi import Request
from core.db.database import session
from settings import templates
from models.db_models import Post
import datetime

templates_router = APIRouter()


@templates_router.get("/")
async def render_html(request: Request):
    """ Main types page. """
    return templates.TemplateResponse("index.html", {"request": request})


@templates_router.get("/type/{key}/")
async def render_html(request: Request, key: str):
    """ Get post with key. """

    post = session.query(Post).filter_by(key=key).first()
    created = str(datetime.datetime.fromtimestamp(post.created).date())

    # TODO: Выпилить created из response

    return templates.TemplateResponse(
        "type.html",
        {"request": request,
         'post': post,
         'created': created})
