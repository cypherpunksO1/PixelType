from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware
from routes.api.router import api_router
from routes.templates.router import templates_router
import settings

app = FastAPI()

app.mount(settings.STATIC_PATH, StaticFiles(directory=settings.STATIC_DIR), name="static")
app.mount(settings.MEDIA_PATH, StaticFiles(directory=settings.MEDIA_DIR), name="media")

app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(api_router, prefix='/api')
app.include_router(templates_router)
