import click

from app.users.constants import Role
from app.users.crud import UserCRUD
from lib.db import session


@click.command()
@click.option("--name", prompt="name", default="admin")
@click.option("--password", prompt="password", default="#P@s$W0Rd!")
def create_superuser(name, password):
    crud = UserCRUD(session())
    crud.create(name=name, password=password, role=Role.ADMIN)


if __name__ == "__main__":
    create_superuser()
