from fastapi import FastAPI
from fastapi import Request, HTTPException
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from core.database import session
from routes.posts import posts_router
from starlette.exceptions import HTTPException as StarletteHTTPException
from models.db_models import Post
import datetime
from settings import errors_description

app = FastAPI()
app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="templates")

app.include_router(posts_router)


@app.exception_handler(StarletteHTTPException)
async def http_exception_handler(request, exc):
    return templates.TemplateResponse("errors/error.html",
                                      {"request": request,
                                       'status_code': exc.status_code,
                                       'detail': errors_description[exc.status_code]})


@app.get("/")
async def render_html(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})


@app.get("/type/{key}/")
async def render_html(request: Request, key: str):
    post = session.query(Post).filter_by(key=key).first()
    try:
        post.created = datetime.datetime.fromtimestamp(post.created).date()
    except TypeError:
        post.created = 'Unknown'

    return templates.TemplateResponse(
        "type.html",
        {"request": request,
         'post': post})
