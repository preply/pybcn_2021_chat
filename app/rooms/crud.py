from sqlalchemy.sql import or_

from app.common.crud import CRUDBase, PaginatedList
from app.rooms.models import Room, Message
from app.users.constants import Lang


class RoomCRUD(CRUDBase):
    model = Room

    def get_multi(
        self,
        query: str = None,
        user_id: str = None,
        sort_by: str = "created_at",
        is_asc: bool = True,
        page: int = 1,
        limit: int = 100,
    ) -> PaginatedList[Room]:
        q = self.db.query(self.model)
        if query:
            q = q.filter(
                or_(
                    self.model.name.ilike(f"%{query}%"),
                )
            )

        if user_id:
            q = q.filter(self.model.users.any(id=user_id))

        return self.paginate(
            query=q, sort_by=sort_by, is_asc=is_asc, page=page, limit=limit
        )

    def add_message(self, room_id: str, user_id: str, text: str, lang: Lang) -> Room:
        self.db.add(Message(room_id=room_id, user_id=user_id, lang=lang, text=text))
        self.db.commit()
        return self.get(room_id)

    def get_first_available(self):
        return self.db.query(self.model).first()
