import factory
import pytest
import random
from sqlalchemy.orm import Session

from tests import faker

from app.rooms.models import Room, Message
from app.users.constants import Lang
from app.users.models import User


class MetaBase:
    sqlalchemy_session_persistence = "commit"


@pytest.fixture(scope="function")
def user_factory(db: Session):
    class UserFactory(factory.alchemy.SQLAlchemyModelFactory):
        class Meta(MetaBase):
            model = User
            sqlalchemy_session = db

        name = factory.Faker("name")
        password = "pass!"
        lang = factory.LazyFunction(lambda: random.choice(list(Lang)))

    return UserFactory


@pytest.fixture(scope="function")
def message_factory(db: Session, room_factory, user_factory):
    class MessageFactory(factory.alchemy.SQLAlchemyModelFactory):
        class Meta(MetaBase):
            model = Message
            sqlalchemy_session = db

        name = factory.Faker("name")
        text = factory.Faker("pystr", min_chars=10, max_chars=1024)
        lang = factory.LazyFunction(lambda: random.choice(list(Lang)))
        room_id = factory.LazyFunction(lambda: room_factory().id)
        user_id = factory.LazyFunction(lambda: user_factory().id)

    return MessageFactory


@pytest.fixture(scope="function")
def room_factory(db: Session, user_factory):
    class RoomFactory(factory.alchemy.SQLAlchemyModelFactory):
        class Meta(MetaBase):
            model = Room
            sqlalchemy_session = db

        name = factory.Faker("name")
        messages = factory.LazyFunction(
            lambda: [
                Message(
                    user_id=user_factory().id,
                    text=faker.pystr(min_chars=10, max_chars=1024),
                    lang=random.choice(list(Lang)),
                )
                for _ in range(5)
            ]
        )

    return RoomFactory
