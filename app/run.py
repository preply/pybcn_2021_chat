import logging
import os
import sys

from loguru import logger
from pydantic import BaseConfig
from fastapi import Request, Response, status, APIRouter, WebSocket, WebSocketDisconnect
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles

from lib.ws import ConnectionManager
from lib.factory import create_app

from app.config import UPLOAD_DIR
from app.common.utils import is_local
from app.common.auth.exceptions import AuthException
from app.common.crud import CRUDException


logger.configure(
    handlers=[
        {
            "sink": sys.stdout,
            "serialize": not is_local(),
            "level": os.environ.get("LOG_LEVEL", logging.DEBUG),
        },
    ],
    # extra={"user": "someone"},
)

BaseConfig.arbitrary_types_allowed = True

app = create_app()
router = APIRouter()
manager = ConnectionManager()


@app.middleware("http")
async def crud_exceptions_wrapper(request: Request, call_next):
    try:
        response = await call_next(request)
    except CRUDException as e:
        return Response(
            content=str(e), status_code=e.status_code or status.HTTP_400_BAD_REQUEST
        )
    except AuthException as e:
        return Response(content=str(e), status_code=status.HTTP_400_BAD_REQUEST)
    return response


if is_local():
    # Mount static folder for local dev
    if not os.path.exists(UPLOAD_DIR):
        os.makedirs(UPLOAD_DIR)
    app.mount("/static", StaticFiles(directory=UPLOAD_DIR), name="static")


@app.get("/")
async def get_chat_page():
    with open('static/chat.html', 'r') as f:
        html = f.read()
    return HTMLResponse(html)


@app.websocket("/ws/{client_id}")
async def websocket_endpoint(websocket: WebSocket, client_id: int):
    await manager.connect(websocket)
    try:
        while True:
            data = await websocket.receive_text()
            await manager.send_personal_message(f"You wrote: {data}", websocket)
            await manager.broadcast(f"Client #{client_id} says: {data}")
    except WebSocketDisconnect:
        manager.disconnect(websocket)
        await manager.broadcast(f"Client #{client_id} left the chat")