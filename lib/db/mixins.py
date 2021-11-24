from datetime import datetime

from sqlalchemy import Column, DateTime
from sqlalchemy.orm import declared_attr


class Dated:
    @declared_attr
    def created_at(cls):
        return Column(DateTime, default=datetime.utcnow, index=True)

    @declared_attr
    def updated_at(cls):
        return Column(DateTime, default=datetime.utcnow, index=True)
