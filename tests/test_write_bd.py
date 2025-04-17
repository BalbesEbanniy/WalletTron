from sqlalchemy import create_engine, StaticPool
from sqlalchemy.orm import sessionmaker
from fastapi.testclient import TestClient
from app.backend.db import Base
from app.backend.db_depends import get_db
from app.models.walletmodel import Wallet
from main import app

TEST_SQLALCHEMY_DATABASE_URL = 'sqlite://'
engine = create_engine(TEST_SQLALCHEMY_DATABASE_URL,
                       connect_args={'check_same_thread': False},
                       poolclass=StaticPool)


TestingSessionLocal = sessionmaker(autoflush=False, bind=engine)


def override_get_db():
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()


app.dependency_overrides[get_db] = override_get_db

Base.metadata.create_all(bind=engine)

test_client = TestClient(app)

def test_get_wallets():
    response = test_client.get('/wallets')
    assert response.status_code == 200
    assert response.json() == []


def test_get_wallets_with_data():
    db = TestingSessionLocal()
    db.add_all([
        Wallet(address = 'T123', bandwidth='123', energy ='123', balance =100),
        Wallet(address = 213, bandwidth=123, energy ='123', balance = 2123)
    ])
    db.commit()

    response = test_client.get('/wallets')
    assert response.status_code == 200
    data = response.json()
    assert len(data) == 2
    assert data[0]['address'] == 'T123'
    assert data[1]['balance'] == 2123