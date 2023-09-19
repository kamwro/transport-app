import pytest
from fastapi import HTTPException
from fastapi.testclient import TestClient
from fastapi.encoders import jsonable_encoder
from fastapi.security import OAuth2PasswordRequestForm
from app.main import app
from app import schemas, dependencies, crud
from app.database import Base, engine_tests
from app.utils import Envs


Base.metadata.create_all(bind=engine_tests)


user1 = schemas.CreateUser(login=Envs.TEST_MAIL, first_name="John",
                        last_name="Tester", address="Cyberworld",
                        is_admin=False, hashed_password="admin123")

user2 = schemas.CreateUser(login="fake_admin", first_name="Victor",
                        last_name="Tester", address="Cyberworld",
                        is_admin=True, hashed_password="admin123")

@pytest.fixture(scope="module")
def client():
    with TestClient(app) as c:
      yield c


@pytest.fixture(scope="module")
def test_user():
    return {"username": user1.login, "password": user1.hashed_password}


@pytest.fixture(scope="module")
def test_admin():
    return {"username": user2.login, "password": user2.hashed_password}

# class override_OAuth2PasswordRequestForm(OAuth2PasswordRequestForm):
#     username = user1.login
#     password = user1.hashed_password


app.dependency_overrides[dependencies.get_db] = dependencies.override_get_db
# app.dependency_overrides[OAuth2PasswordRequestForm] = override_OAuth2PasswordRequestForm

# active_user = dependencies.get_current_active_user(schemas.User(login=Envs.TEST_MAIL_1, first_name="John",
#                         last_name="Tester", address="Cyberworld",
#                         is_admin=False, hashed_password="admin123"))


# client = TestClient(app)

def test_create_user():
    user = user1
    user = jsonable_encoder(user)
    response = client.post("/users/", json = user)
    assert response.status_code == 200, response.text
    assert response.json()['message'] == f"activation link has been sent to {user['login']}"


def test_create_user_admin():
    user = user2
    user = jsonable_encoder(user)
    response = client.post("/users/", json = user)
    assert response.status_code == 200
    assert response.json()['message'] == "user is a superuser. Automatic account activation."


def test_create_user_email_already_registered():
    user = user1
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


def test_login(client, test_user):
    response = client.post("/login", data=test_user)
    assert response.status_code == 200
    token = response.json()["access_token"]
    assert token is not None
    return token

def test_read_my_info_not_active():
    token = test_login(client, test_user)
    response = client.get("/users/me/", headers={"Authorization": f"Bearer {token}"})
    assert response.status_code == 401
    assert response.json() == "Inactive user"


def test_send_activation_code():
    token = test_login(client, test_user)
    response = client.get("/users/me/send-activation-code", headers={"Authorization": f"Bearer {token}"})
    assert response.status_code == 200
    assert response.json()['message'] == f"activation code has been sent to {user1.login}"


def test_send_activation_code_not_logged_in():
    response = client.get("/users/me/send-activation-code")
    assert response.status_code == 401


def test_activate_my_account_incorrect_code():
    token = test_login(client, test_user)
    response = client.get(f"users/1/activate/fake-code",
                          headers={"Authorization": f"Bearer {token}"})
    assert response.status_code == 401
    assert response.json() == {"detail": "Login is not a valid email address."}


def test_activate_my_account():
    token = test_login(client, test_user)
    response = client.get(f"users/1/activate/{crud.get_user_by_login(db=dependencies.override_get_db(), user_login=user1.login).activation_code}",
                          headers={"Authorization": f"Bearer {token}"})
    assert response.status_code == 200
    assert response.json()['message'] == "your account has been activated."


def test_activate_my_account_not_logged_in():
    response = client.get(f"users/1/activate/{crud.get_user_by_login(db=dependencies.override_get_db(), user_login=user1.login).activation_code}")
    assert response.status_code == 401


def test_send_activation_code_already_active():
    token = test_login(client, test_user)
    response = client.get("/users/me/send-activation-code", headers={"Authorization": f"Bearer {token}"})
    assert response.status_code == 405
    assert response.json() == {"detail": "User already active"}


def test_activate_my_account_already_active():
    token = test_login(client, test_user)
    response = client.get(f"users/1/activate/{crud.get_user_by_login(db=dependencies.override_get_db(), user_login=user1.login).activation_code}",
                          headers={"Authorization": f"Bearer {token}"})
    assert response.status_code == 405
    assert response.json() == {"detail": "User already active"}


def test_read_my_info():
    token = test_login(client, test_user)
    response = client.get("/users/me/", headers={"Authorization": f"Bearer {token}"})
    assert response.status_code == 200
    assert response.json() == [crud.get_user_by_login(db=dependencies.override_get_db(), user_login=user1.login)]


def test_view_user_info_not_an_admin():
    token = test_login(client, test_user)
    response = client.get(f"users/adm/{user1.login}", headers={"Authorization": f"Bearer {token}"})
    assert response.status_code == 401


def test_view_user_info():
    token = test_login(client, test_admin)
    response = client.get(f"users/adm/{user1.login}", headers={"Authorization": f"Bearer {token}"})
    assert response.status_code == 200
    assert response.json() == [crud.get_user_by_login(db=dependencies.override_get_db(), user_login=user1.login)]


def test_view_user_info_no_user():
    token = test_login(client, test_admin)
    response = client.get(f"users/adm/{user1.login}", headers={"Authorization": f"Bearer {token}"})
    assert response.status_code == 405
    assert response.json() == {"detail": "There's no user with email = totally-fake-login"}


def test_remove_adm_not_an_admin():
    token = test_login(client, test_user)
    response = client.get(f"users/adm/{user1.login}/remove-adm", headers={"Authorization": f"Bearer {token}"})
    assert response.status_code == 401 


def test_remove_adm_no_user():
    token = test_login(client, test_admin)
    response = client.get(f"users/adm/totally-fake-login/remove-adm", headers={"Authorization": f"Bearer {token}"})
    assert response.status_code == 405
    assert response.json() == {"detail": "There's no user with email = totally-fake-login"}


def test_remove_adm_user_not_an_admin():
    token = test_login(client, test_admin)
    response = client.get(f"users/adm/{user1.login}/remove-adm", headers={"Authorization": f"Bearer {token}"})
    assert response.status_code == 405 
    assert response.json() == {"detail": "User not an admin"}


def test_grant_adm_no_user():
    token = test_login(client, test_admin)
    response = client.get(f"users/adm/totally-fake-login/grant-adm", headers={"Authorization": f"Bearer {token}"})
    assert response.status_code == 405
    assert response.json() == {"detail": "There's no user with email = totally-fake-login"}


def test_grant_adm_not_an_admin():
    token = test_login(client, test_user)
    response = client.get(f"users/adm/{user1.login}/grant-adm", headers={"Authorization": f"Bearer {token}"})
    assert response.status_code == 401 


def test_grant_adm():
    token = test_login(client, test_admin)
    response = client.get(f"users/adm/{user1.login}/grant-adm", headers={"Authorization": f"Bearer {token}"})
    assert response.status_code == 200 
    assert response.json() == [crud.get_user_by_login(db=dependencies.override_get_db(), user_login=user1.login)]


def test_grant_adm_user_already_an_admin():
    token = test_login(client, test_admin)
    response = client.get(f"users/adm/{user1.login}/grant-adm", headers={"Authorization": f"Bearer {token}"})
    assert response.status_code == 405 
    assert response.json() == {"detail": "User already an admin"}


def test_remove_adm():
    token = test_login(client, test_admin)
    response = client.get(f"users/adm/{user1.login}/remove-adm", headers={"Authorization": f"Bearer {token}"})
    assert response.status_code == 200 
    assert response.json() == [crud.get_user_by_login(db=dependencies.override_get_db(), user_login=user1.login)]


# def test_deactivate_user_not_an_admin():
#     pass


# def test_deactivate_user_no_user():
#     pass


# def test_deactivate_user():
#     pass


# def test_deactivate_user_user_already_inactive():
#     pass


# def test_activate_user():
#     pass


# def test_activate_user_not_an_admin():
#     pass


# def test_activate_user_no_user():
#     pass


# def test_activate_user_user_already_active():
#     pass


# def test_delete_user_not_an_admin():
#     pass


# def test_delete_user():
#     pass


# def test_delete_user_no_user():
#     pass


# def test_delete_my_account():
#     pass