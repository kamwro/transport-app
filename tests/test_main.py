import pytest
from fastapi import HTTPException
from fastapi.testclient import TestClient
from fastapi.security import OAuth2PasswordRequestForm
from fastapi.encoders import jsonable_encoder
from app.main import app
from app import schemas, dependencies
from app.database import Base, engine_tests


Base.metadata.create_all(bind=engine_tests)

app.dependency_overrides[dependencies.get_db] = dependencies.override_get_db



client = TestClient(app)


def test_welcome_to_the_app():
    response = client.get("/")
    assert response.status_code == 200, response.text
    assert response.json()['message'] == "Hello world! Go to the /docs."


def test_login_for_access_token():
    response = client.post("/token")
    assert response.status_code == 200, response.text
    assert "access_token" in response.json()['message']
    assert "token_type" in response.json()['message'] 


def test_login_for_access_token_bad_credentials():
    pass