from app.config import ENV
from fastapi.templating import Jinja2Templates


templates = Jinja2Templates(directory="templates")


def is_local():
    return ENV == "local"
