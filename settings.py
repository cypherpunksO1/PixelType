from fastapi.templating import Jinja2Templates

errors_description = {
    404: "Oops! Looks like you took a wrong turn. This page seems to be missing.",
    500: "Uh-oh! Something went wrong on our end. Our team of highly trained monkeys is working to fix it."
}

templates = Jinja2Templates(directory="templates")

origins = [
    "http://localhost",
    "http://localhost:8080",
    "http://127.0.0.1:8000",
    "http://127.0.0.1:80", 
    "https://pixeltype.egoryolkin.ru",
    "https://pixeltype.egoryolkin.ru:8000"
]

