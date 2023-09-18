import pytest
from fastapi import HTTPException
from fastapi.testclient import TestClient
from fastapi.encoders import jsonable_encoder
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool
from ..routers.users import router
from .. import schemas, dependencies
from ..database import Base, SQLALCHEMY_DATABASE_URL

engine = create_engine(
    SQLALCHEMY_DATABASE_URL,
    connect_args={"check_same_thread": False},
    poolclass=StaticPool,
)

TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base.metadata.create_all(bind=engine)

def override_get_db():
    try:
        db = TestingSessionLocal()
        yield db
    finally:
        db.close()

router.dependency_overrides[dependencies.get_db] = override_get_db

client = TestClient(router)


def test_create_user():
    user_data =     {
  "login": "fake@email.fake",
  "first_name": "John",
  "last_name": "Tester",
  "address": "Cyberworld",
  "is_admin": False,
  "hashed_password": "admin123"
}
    response = client.post("/", json = {user_data})
    assert response.status_code == 200
    user_data = {info:user_data[info] for info in user_data if info!='hashed_password'}
    assert response.json() == {"user data: ": [user_data], "message": f"activation code has been sent to {user_data['login']}"}

def test_create_user_admin():
    user_data =     {
  "login": "fake_admin",
  "first_name": "Victor",
  "last_name": "Tester",
  "address": "Cyberworld",
  "is_admin": True,
  "hashed_password": "admin123"
}
    response = client.post("/", json = {user_data})
    assert response.status_code == 200
    user_data = {info:user_data[info] for info in user_data if info!='hashed_password'}
    assert response.json() == {"user data: ": [user_data], "message": "user is a superuser. Automatic account activation."}

def test_create_user_email_already_registered():
    with pytest.raises(HTTPException) as e:
        user_data =     {
    "login": "fake@email.fake",
    "first_name": "Fake John",
    "last_name": "Tester",
    "address": "Yesterdays",
    "is_admin": False,
    "hashed_password": "admin123"
    }
        response = client.post("/", json = {user_data})
        assert response.status_code == 405
        assert "Email already registered" in str(e.value)

def test_create_user_email_not_valid():
    with pytest.raises(HTTPException) as e:
        user_data =     {
    "login": "fake@",
    "first_name": "Arnold",
    "last_name": "Tester",
    "address": "Westworld",
    "is_admin": False,
    "hashed_password": "admin123"
    }
        response = client.post("/", json = {user_data})
        assert response.status_code == 405
        assert "Login is not a valid email address." in str(e.value)