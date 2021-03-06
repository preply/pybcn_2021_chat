from app.common.crud import CRUDBase, PaginatedList
from app.users.models import User


class UserCRUD(CRUDBase):
    model = User

    def get_or_create(self, **kwargs):
        user = self.db.query(self.model).filter_by(**kwargs).first()
        if not user:
            user = self.create(**kwargs)
        return user

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
            q = q.filter(User.name.ilike(f"%{query}%"))

        return self.paginate(
            query=q, sort_by=sort_by, is_asc=is_asc, page=page, limit=limit
        )
