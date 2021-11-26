import click

from app.users.crud import UserCRUD
from lib.db import session


@click.command()
@click.option("--name", prompt="name", default="admin")
def create_superuser(name):
    UserCRUD(session()).create(name=name)


if __name__ == "__main__":
    create_superuser()
