from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from app.config import SQLALCHEMY_DATABASE_URI


engine = create_engine(SQLALCHEMY_DATABASE_URI, pool_pre_ping=True)
session = sessionmaker(autocommit=False, autoflush=False, bind=engine)
