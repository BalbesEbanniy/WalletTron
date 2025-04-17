from app.backend.db import Base
from sqlalchemy import Column, Integer, String, DECIMAL

#db model
class Wallet(Base):
    __tablename__ = 'wallets'

    id = Column(Integer, primary_key=True)
    address = Column(String(40), nullable=False)
    bandwidth = Column(Integer)
    energy = Column(Integer)
    balance = Column(DECIMAL)