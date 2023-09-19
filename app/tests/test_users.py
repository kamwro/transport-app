import pytest
from fastapi import HTTPException
from fastapi.testclient import TestClient
from fastapi.encoders import jsonable_encoder
from fastapi.security import OAuth2PasswordRequestForm
from ..main import app
from .. import schemas, dependencies
from ..database import Base, engine_tests
from ..utils import Envs


Base.metadata.create_all(bind=engine_tests)

class override_OAuth2PasswordRequestForm(OAuth2PasswordRequestForm):
    username = Envs.TEST_MAIL_1
    password = "admin123"
    

app.dependency_overrides[dependencies.get_db] = dependencies.override_get_db
app.dependency_overrides[OAuth2PasswordRequestForm] = override_OAuth2PasswordRequestForm

# active_user = dependencies.get_current_active_user(schemas.User(login=Envs.TEST_MAIL_1, first_name="John",
#                         last_name="Tester", address="Cyberworld",
#                         is_admin=False, hashed_password="admin123"))


client = TestClient(app)


def test_create_user():
    user = schemas.CreateUser(login=Envs.TEST_MAIL_1, first_name="John",
                        last_name="Tester", address="Cyberworld",
                        is_admin=False, hashed_password="admin123")
    user = jsonable_encoder(user)
    response = client.post("/users/", json = user)
    assert response.status_code == 200, response.text
    assert response.json()['message'] == f"activation code has been sent to {user['login']}"


def test_create_user_admin():
    user = schemas.CreateUser(login="fake_admin", first_name="Victor",
                        last_name="Tester", address="Cyberworld",
                        is_admin=True, hashed_password="admin123")
    user = jsonable_encoder(user)
    response = client.post("/users/", json = user)
    assert response.status_code == 200
    assert response.json()['message'] == "user is a superuser. Automatic account activation."


def test_create_user_email_already_registered():
    user = schemas.CreateUser(login=Envs.TEST_MAIL_1, first_name="Fake John",
                        last_name="Tester", address="Yesterdays",
                        is_admin=False, hashed_password="admin123")
    user = jsonable_encoder(user)
    response = client.post("/users/", json = user)
    assert response.status_code == 405
    assert response.json() == {"detail": "Email already registered"}


def test_create_user_email_not_valid():
    user = schemas.CreateUser(login="fake@", first_name="Arnold",
                            last_name="Tester", address="Westworld",
                            is_admin=False, hashed_password="admin123")
    user = jsonable_encoder(user)
    response = client.post("/users/")
    assert response.status_code == 405
    assert response.json() == {"detail": "Login is not a valid email address."}


def test_read_my_info():
    response = client.get("/users/me/")
    assert response.status_code == 200
    assert response.json()['message'] == "user is a superuser. Automatic account activation."


# def test_read_my_info_not_active():
#     pass


# def test_send_activation_code():
#     pass


# def test_send_activation_code_not_logged_in():
#     pass


# def test_send_activation_code_already_active():
#     pass


# def test_activate_my_account():
#     pass


# def test_activate_my_account_not_logged_in():
#     pass


# def test_activate_my_account_already_active():
#     pass


# def test_activate_my_account_incorrect_code():
#     pass


# def test_delete_my_account():
#     pass