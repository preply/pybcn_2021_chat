from app.config import ENV


def is_local():
    return ENV == "local"
