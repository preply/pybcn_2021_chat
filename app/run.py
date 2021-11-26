import os
from fastapi import Request, Response, status
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware

from lib.factory import create_app

from app.config import STATIC_DIR
from app.common.crud import CRUDException


app = create_app()

origins = [
    "http://localhost",
    "http://localhost:3000",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.middleware("http")
async def crud_exceptions_wrapper(request: Request, call_next):
    try:
        response = await call_next(request)
    except CRUDException as e:
        return Response(
            content=str(e), status_code=e.status_code or status.HTTP_400_BAD_REQUEST
        )
    return response


if not os.path.exists(STATIC_DIR):
    os.makedirs(STATIC_DIR)
app.mount("/static", StaticFiles(directory=STATIC_DIR), name="static")
