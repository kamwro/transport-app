import pytest
from fastapi import HTTPException
from fastapi.testclient import TestClient
from fastapi.security import OAuth2PasswordRequestForm
from fastapi.encoders import jsonable_encoder
from ..main import app
from .. import schemas, dependencies
from ..database import Base, engine_tests


Base.metadata.create_all(bind=engine_tests)

app.dependency_overrides[dependencies.get_db] = dependencies.override_get_db



client = TestClient(app)


def test_welcome_to_the_app():
    response = client.get("/")
    assert response.status_code == 200, response.text
    assert response.json()['message'] == "Hello world! Go to the /docs."


# def test_login_for_access_token():
#     pass


# def test_login_for_access_token_bad_credentials():
#     pass