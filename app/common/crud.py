import logging
from datetime import datetime
from typing import Union

from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session, Query

from app.common.utils import is_null_error, in_error


logger = logging.getLogger(__name__)


class PaginatedList(list):
    def __init__(self, *args, query: Query = None):
        self.query = query
        super(PaginatedList, self).__init__(*args)


class CRUDBase:
    model = NotImplemented

    def __init__(self, db: Session):
        self.db = db
        self.name = self.model.__name__

    def save(self, obj):
        """Redefine to implement custom saving logic"""
        self.db.add(obj)
        try:
            self.db.commit()
        except IntegrityError as e:
            self.db.rollback()

            if is_null_error(e):
                raise CRUDException("Required fields are empty")

            if in_error(e, text="already exists"):
                raise CRUDException("Already exists")

            raise
        return obj

    def delete(self, pk: Union[int, str]):
        obj = self.get(pk, silent=False)
        self.db.delete(obj)
        try:
            self.db.commit()
        except IntegrityError:
            self.db.rollback()
            msg = f"Cannot delete {self.name}:{id}"
            logger.warning(msg)
            raise CRUDException(msg)

        logger.info("Deleted %s:%s", self.name, id)

        return obj

    def get(self, pk: Union[int, str, list], silent=True):
        if pk and isinstance(pk, list):
            res = self.db.query(self.model).filter(self.model.id.in_(pk)).all()
        elif pk:
            res = self.db.query(self.model).get(pk)
        else:
            raise CRUDException("Empty id")

        if not (res or silent):
            raise DoesNotExistException(f"Does not exist {self.name}:{pk}")

        return res

    def create(self, **kwargs):
        obj = self.model(**kwargs)
        self.save(obj)
        self.db.refresh(obj)
        logger.info("Created %s:%s", self.name, obj.id)
        return obj

    def update(self, pk: Union[int, str], ignore_unset: bool = False, **kwargs):
        obj = self.get(pk, silent=False)

        if hasattr(obj, "updated_at"):
            obj.updated_at = datetime.utcnow()

        for field, value in kwargs.items():
            if value is not None or not ignore_unset:
                setattr(obj, field, value)

        self.save(obj)

        self.db.refresh(obj)
        return obj

    def paginate(
        self, query: Query, sort_by: str, is_asc: bool, page: int, limit: int
    ) -> PaginatedList:
        order_field = getattr(self.model, sort_by)
        if not is_asc:
            order_field = order_field.desc()
        offset = (page - 1) * limit

        return PaginatedList(
            query.order_by(order_field).offset(offset).limit(limit).all(),
            query=query,
        )


class CRUDException(Exception):
    def __init__(self, msg, status_code=None):
        self.msg = msg
        self.status_code = status_code


class DoesNotExistException(CRUDException):
    def __init__(self, msg):
        self.msg = msg
        self.status_code = 404
