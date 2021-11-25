from sqlalchemy.orm import Session
from fastapi import (
    Depends,
    APIRouter,
    WebSocket,
    WebSocketDisconnect,
    Request,
    HTTPException,
)
from fastapi.responses import HTMLResponse

from lib.ws import ConnectionManager

from app.common.utils import templates
from app.common import deps
from app.users.models import User
from app.rooms.crud import RoomCRUD


router = APIRouter(prefix="/chat")
manager = ConnectionManager()


@router.get("/", response_class=HTMLResponse)
async def get_chat_page(
    request: Request,
    db: Session = Depends(deps.get_db),
    current_user: User = Depends(deps.get_current_user),
):
    room = RoomCRUD(db).get_or_create_first_available()
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
    current_user: User = Depends(deps.get_websocket_user),
    db: Session = Depends(deps.get_db),
):
    await manager.connect(user=current_user, websocket=websocket)
    try:
        while True:
            data = await websocket.receive_text()
            message = RoomCRUD(db).add_message(
                room_id=room_id,
                user_id=current_user.id,
                text=data,
                lang=current_user.lang,
            )
            await manager.broadcast(message=message)
    except WebSocketDisconnect:
        manager.disconnect(current_user.id)
