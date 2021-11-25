from dataclasses import dataclass
from typing import Dict
from fastapi import WebSocket

from app.rooms.utils import translate
from app.users.constants import Lang
from app.users.models import User


@dataclass
class UserConnection:
    socket: WebSocket
    lang: Lang


class ConnectionManager:
    def __init__(self):
        self.active_connections: Dict[str, UserConnection] = {}

    async def connect(self, user: User, websocket: WebSocket):
        await websocket.accept()
        self.active_connections[user.id] = UserConnection(
            socket=websocket, lang=user.lang
        )

    def disconnect(self, user_id: str):
        self.active_connections.pop(user_id)

    async def broadcast(self, message: str, user: User):
        for conn in self.active_connections.values():
            text = translate(text=message, from_lang=user.lang, to_lang=conn.lang)
            await conn.socket.send_text(f"User #{user.name}: {text}")
