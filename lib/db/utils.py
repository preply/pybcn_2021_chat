from furl import furl
from sqlalchemy import create_engine
from loguru import logger

from lib.db import session, Base
from lib.db.session import engine


def is_db_exists(dsn: str):
    name = get_db_name(dsn)
    query = "SELECT datname FROM pg_database WHERE datistemplate = false;"
    conn = get_db_engine(dsn).connect()
    names = {row[0] for row in conn.execute(query).fetchall()}
    conn.close()
    return name in names


def create_db(dsn: str):
    name = get_db_name(dsn)
    if not is_db_exists(dsn):
        logger.info("Creating DB:{name}...", name=name)
        conn = get_db_engine(dsn).connect()
        conn.execute("CREATE DATABASE %s;" % name)
        conn.close()


def drop_db(dsn: str):
    name = get_db_name(dsn)
    if is_db_exists(dsn):
        logger.info("Dropping DB:{name}...", name=name)
        conn = get_db_engine(dsn).connect()
        conn.execute("DROP DATABASE %s;" % name)
        conn.close()


def create_tables():
    conn = session().connection()
    table_names = engine.dialect.get_table_names(connection=conn)
    if not table_names:
        logger.info("Creating tables...")
        Base.metadata.create_all(bind=engine)
    else:
        logger.info("Tables are already created {names} ", names=table_names)


def truncate_all_tables():
    db = session()
    for table in reversed(Base.metadata.sorted_tables):
        logger.info("Clear table:{name}", name=table)
        db.execute(table.delete())  # Truncate table
    db.commit()


def get_db_engine(dsn):
    url = furl(dsn)
    db_name = url.path.segments[0]
    url.path.remove(db_name)  # Remove database name from DSN
    return create_engine(url.url, isolation_level="AUTOCOMMIT")


def get_db_name(dsn: str) -> str:
    url = furl(dsn)
    return url.path.segments[0]
