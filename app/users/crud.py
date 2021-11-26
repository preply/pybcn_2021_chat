from sqlalchemy.sql import or_

from app.common.crud import CRUDBase, PaginatedList
from app.users.models import User


class UserCRUD(CRUDBase):
    model = User

    def get_multi(
        self,
        query: str = None,
        sort_by: str = "created_at",
        is_asc: bool = True,
        page: int = 1,
        limit: int = 100,
    ) -> PaginatedList[User]:
        q = self.db.query(User)
        if query:
            q = q.filter(
                or_(
                    User.name.ilike(f"%{query}%"),
                )
            )

        return self.paginate(
            query=q, sort_by=sort_by, is_asc=is_asc, page=page, limit=limit
        )
