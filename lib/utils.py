import random
import string
import uuid
from datetime import timedelta, datetime
from decimal import Decimal


def dcml(val) -> Decimal:
    return Decimal(str(val))


def percent(val) -> Decimal:
    return dcml(val) * dcml(0.01)


def from_now(days: int = 30) -> datetime:
    return datetime.utcnow() + timedelta(days)


def get_random_uuid() -> str:
    return str(uuid.uuid4())


def get_random_string(n: int = 6) -> str:
    return "".join(random.choices(string.ascii_uppercase + string.digits, k=n))
