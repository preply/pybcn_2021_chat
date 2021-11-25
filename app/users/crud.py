from sqlalchemy.sql import or_

from app.config import SECRET_KEY
from app.common.crud import CRUDBase, PaginatedList
from app.users.constants import Role
from app.users.models import User
from app.users.utils import hash_password


class UserCRUD(CRUDBase):
    model = User

    def get_by_cred(self, name: str, password) -> User:
        user = (
            self.db.query(User)
            .filter(
                User.name == name,
                User.password == hash_password(salt=SECRET_KEY, password=password),
            )
            .first()
        )
        return user

    def get_multi(
        self,
        query: str = None,
        role: Role = None,
        is_active: bool = None,
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

        if role:
            q = q.filter(User.role == role)

        if is_active is not None:
            q = q.filter(User.is_active == is_active)

        return self.paginate(
            query=q, sort_by=sort_by, is_asc=is_asc, page=page, limit=limit
        )
