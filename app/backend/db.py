from sqlalchemy import Column, Integer, String, DECIMAL, Nullable
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, DeclarativeBase


engine = create_engine('sqlite:///base.db', echo=True)
SessionLocal = sessionmaker(bind=engine)

class Base(DeclarativeBase):
    pass
