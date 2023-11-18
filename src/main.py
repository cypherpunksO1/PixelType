from fastapi import (FastAPI, 
                     HTTPException)
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware

from src.routers import (get_api_routers,
                         get_templates_router)

from core.conf import config

app = FastAPI(title="PixelType", 
              debug=config.DEBUG, 
              description="Anonimous articles service", 
              version="1.5")

app.mount(config.STATIC_PATH, StaticFiles(directory=config.STATIC_DIR), name="static")
app.mount(config.MEDIA_PATH, StaticFiles(directory=config.MEDIA_DIR), name="media")

app.add_middleware(
    CORSMiddleware,
    allow_origins=config.ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.exception_handler(HTTPException)
async def http_exception_handler(request, exc):
    """
        Exceptions handler.
        Redirect to errors/error.html with status_code & detail.
    """
    return templates.TemplateResponse("errors/error.html",
                                      {"request": request,
                                       'status_code': exc.status_code,
                                       'detail': errors_description[exc.status_code]})


app.include_router(get_api_routers())
app.include_router(get_templates_router())
