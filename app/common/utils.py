from app.config import ENV


def is_local():
    return ENV == "local"


def is_null_error(e: Exception):
    return "null value in column" in str(e)


def in_error(e: Exception, text: str):
    return text in str(e)
