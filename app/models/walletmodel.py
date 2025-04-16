from app.backend.db import Base
from sqlalchemy import Column, Integer, String, DECIMAL


class Wallet(Base):
    __tablename__ = 'wallets'

    id = Column(Integer, primary_key=True)
    address = Column(String(40), nullable=False)
    bandwidth = Column(Integer)
    energy = Column(Integer)
    balance = Column(DECIMAL)

from sqlalchemy.schema import CreateTable
print(CreateTable(Wallet.__table__))
