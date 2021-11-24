import os

PROJECT_NAME = "chat"

API_PREFIX = "/api"

ENV = os.environ.get("ENV", "local")

AUTH_COOKIE_NAME = os.environ.get("AUTH_COOKIE_NAME", "SID")
AUTH_TTL = 3600 * 24
DEVICE_ID_HEADER_NAME = os.environ.get("DEVICE_ID_HEADER_NAME", "X-Client-Token")
AUTH_SESSION_TTL = os.environ.get("AUTH_SESSION_TTL", 24 * 3600 * 365)

SQLALCHEMY_TRACK_MODIFICATIONS = False

STATIC_DIR = "static"

POSTGRES_USER = os.environ.get("POSTGRES_USER")
POSTGRES_PASSWORD = os.environ.get("POSTGRES_PASSWORD")
POSTGRES_DB = os.environ.get("POSTGRES_DB")
POSTGRES_HOST = os.environ.get("POSTGRES_HOST", "chat-db")
POSTGRES_PORT = os.environ.get("POSTGRES_PORT", "5432")

SQLALCHEMY_DATABASE_URI = f"postgresql+psycopg2://{POSTGRES_USER}:{POSTGRES_PASSWORD}@{POSTGRES_HOST}:{POSTGRES_PORT}/{POSTGRES_DB}"
SECRET_KEY = os.environ.get("SECRET_KEY")

REDIS_HOST = os.environ.get("REDIS_HOST", "chat-redis")
REDIS_PORT = os.environ.get("REDIS_PORT", 6379)
REDIS_DB = os.environ.get("REDIS_DB", 0)
