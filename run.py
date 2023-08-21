from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from routes.api.v1.posts import posts_router
from routes.templates.main import templates_router

app = FastAPI()

app.mount("/static", StaticFiles(directory="static"), name="static")


app.include_router(posts_router)
app.include_router(templates_router)
