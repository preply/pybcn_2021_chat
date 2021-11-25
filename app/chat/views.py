from sqlalchemy.orm import Session
from fastapi import Depends, APIRouter, WebSocket, WebSocketDisconnect, Request
from fastapi.responses import HTMLResponse

from lib.ws import ConnectionManager

from app.config import AUTH_COOKIE_NAME
from app.common.utils import templates
from app.common.auth import utils as auth
from app.common import deps
from app.users.models import User
from app.users.crud import UserCRUD
from app.rooms.crud import RoomCRUD


router = APIRouter(prefix="/chat")
manager = ConnectionManager()


@router.get("/", response_class=HTMLResponse)
async def get_chat_page(
    request: Request,
    db: Session = Depends(deps.get_db),
    current_user: User = Depends(deps.get_current_user),
):
    room = RoomCRUD(db).get_first_available()
    return templates.TemplateResponse(
        "chat.html",
        {
            "request": request,
            "room_id": room.id,
            "room_name": room.name,
            "user_name": current_user.name,
        },
    )


@router.websocket("/ws/{room_id}")
async def websocket_endpoint(
    room_id: str,
    websocket: WebSocket,
    db: Session = Depends(deps.get_db),
):
    token = websocket.cookies.get(AUTH_COOKIE_NAME)
    user_id = auth.get_user_id(token)
    user = UserCRUD(db).get(user_id) if user_id else None
    if not user or not user.is_active:
        # TODO: Register new one or raise an error?
        pass

    await manager.connect(user=user, websocket=websocket)
    try:
        while True:
            data = await websocket.receive_text()
            RoomCRUD(db).add_message(
                room_id=room_id, user_id=user.id, text=data, lang=user.lang
            )
            await manager.broadcast(message=data, user=user)
    except WebSocketDisconnect:
        manager.disconnect(user.id)
        await manager.broadcast(f"User #{user.name} left the chat")
