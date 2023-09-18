import pytest
from fastapi import HTTPException
from fastapi.testclient import TestClient
from fastapi.encoders import jsonable_encoder
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool
from ..main import app
from .. import schemas, dependencies
from ..database import Base

engine = create_engine(
    "sqlite://",
    connect_args={"check_same_thread": False},
    poolclass=StaticPool
)

TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base.metadata.create_all(bind=engine)

def override_get_db():
    try:
        db = TestingSessionLocal()
        yield db
    finally:
        db.close()

app.dependency_overrides[dependencies.get_db] = override_get_db

client = TestClient(app)

#main

# def test_welcome_to_the_app():
#     pass

# def test_login_for_access_token():
#     pass

# def test_login_for_access_token_bad_credentials():
#     pass

#users

def test_create_user():
    user = schemas.CreateUser(login="fake@email.fake", first_name="John",
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
    user = schemas.CreateUser(login="fake@email.fake", first_name="Fake John",
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
    response = client.post("/users/", json = user)
    assert response.status_code == 405
    assert response.json() == {"detail": "Login is not a valid email address."}

# def test_read_my_info():
#     pass

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

# #admin - users

# def test_view_user_info():
#     pass

# def test_view_user_info_not_an_admin():
#     pass

# def test_view_user_info_no_user():
#     pass

# def test_grant_adm():
#     pass

# def test_grant_adm_not_an_admin():
#     pass

# def test_grant_adm_no_user():
#     pass

# def test_grant_adm_user_already_an_admin():
#     pass

# def test_remove_adm():
#     pass

# def test_remove_adm_not_an_admin():
#     pass

# def test_remove_adm_no_user():
#     pass

# def test_remove_adm_user_not_an_admin():
#     pass

# def test_activate_user():
#     pass

# def test_activate_user_not_an_admin():
#     pass

# def test_activate_user_no_user():
#     pass

# def test_activate_user_user_already_active():
#     pass

# def test_deactivate_user():
#     pass

# def test_deactivate_user_not_an_admin():
#     pass

# def test_deactivate_user_no_user():
#     pass

# def test_deactivate_user_user_already_inactive():
#     pass

# def test_delete_user():
#     pass

# def test_delete_user_not_an_admin():
#     pass

# def test_delete_user_no_user():
#     pass

#rides

# def test_reserve_ride():
#     pass

# def test_reserve_ride_user_not_active():
#     pass

# def test_reserve_ride_no_ride():
#     pass

# def test_reserve_ride_inactive_ride():
#     pass

# def test_get_all_rides():
#     pass

# def test_get_all_rides_no_rides():
#     pass

# def test_get_all_rides_by_starting_city_no_rides():
#     pass

# def test_get_all_rides_by_destination_city_no_rides():
#     pass

# def test_get_all_rides_from_one_city_to_another():
#     pass

# def test_get_all_rides_from_one_city_to_another_no_rides():
#     pass

# #adm - rides

# def test_create_ride():
#     pass

# def test_archivise_ride():
#     pass

# def test_archivise_ride_no_ride():
#     pass

# def test_archivise_ride_ride_already_inactive():
#     pass

# def test_delete_ride():
#     pass

# def test_delete_ride_no_ride():
#     pass
