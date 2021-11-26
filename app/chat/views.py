from sqlalchemy.orm import Session
from fastapi import (
    Depends,
    APIRouter,
    WebSocket,
    WebSocketDisconnect,
)

from app.users.crud import UserCRUD
from lib.ws import ConnectionManager

from app.common import deps
from app.rooms.crud import RoomCRUD


router = APIRouter(prefix="/chat")
manager = ConnectionManager()


@router.websocket("/ws/{room_id}")
async def websocket_endpoint(
    room_id: str,
    websocket: WebSocket,
    db: Session = Depends(deps.get_db),
):
    await manager.connect(user=user, websocket=websocket)
    try:
        while True:
            data = await websocket.receive_json()
            user = UserCRUD(db).get(data["userId"])
            message = RoomCRUD(db).add_message(
                room_id=room_id,
                user_id=user.id,
                text=data["message"],
                lang=user.lang,
            )
            await manager.broadcast(message=message)
    except WebSocketDisconnect:
        manager.disconnect(user.id)
