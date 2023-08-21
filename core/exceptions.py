from starlette.exceptions import HTTPException as StarletteHTTPException
from settings import errors_description
from settings import templates
from run import app


@app.exception_handler(StarletteHTTPException)
async def http_exception_handler(request, exc):
    """
        Exceptions handler.
        Redirect to errors/error.html with status_code & detail.
    """
    return templates.TemplateResponse("errors/error.html",
                                      {"request": request,
                                       'status_code': exc.status_code,
                                       'detail': errors_description[exc.status_code]})
