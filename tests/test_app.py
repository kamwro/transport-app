import pytest
from fastapi.encoders import jsonable_encoder
from app.main import app
from app import schemas, dependencies
from app.database import Base, engine_tests


Base.metadata.create_all(bind=engine_tests)


app.dependency_overrides[dependencies.get_db] = dependencies.override_get_db


# all tests except activate_my_account - needs to figure out how to write it


def test_welcome_to_the_app(client):
    """Trying:
        get("/")

    Expecting: 
        status code: 200 (OK)

        message: "Hello world! Go to the /docs."

    Args:
        client (Generator): yields test client
    """
    response = client.get("/")
    assert response.status_code == 200, response.text
    assert response.json()['message'] == "Hello world! Go to the /docs."


def test_create_user(client, test_user_schema):
    """Trying:
        post("/users/") user not an admin

    Expecting: 
        status code: 200 (OK)
        
        response with message: "activation link has been sent to <login>"

    Args:
        client (Generator): yields test client
        test_user_schema (schema.CreateUser): user data
    """
    user = test_user_schema
    user = jsonable_encoder(user)
    response = client.post("/users/", json = user)
    assert response.status_code == 200
    assert response.json()['message'] == f"activation link has been sent to {user['login']}"


def test_create_user_email_already_registered(client, test_user_schema):
    """Trying:
        post("/users/") using login that is already registered

    Expecting: 
        status code: 405 (Method Not Allowed)
        
        raises an exception with detail: "Email already registered"

    Args:
        client (Generator): yields test client
        test_user_schema (schema.CreateUser): user data
    """
    user = test_user_schema
    user = jsonable_encoder(user)
    response = client.post("/users/", json = user)
    assert response.status_code == 405
    assert response.json() == {"detail": "Email already registered"}


def test_create_user_admin(client, test_admin_schema):
    """Trying:
        post("/users/") specifying that we want to create an admin account

    Expecting: 
        status code: 200 (OK)
        
        response with message: "user is a superuser. Automatic account activation."

    Args:
        client (Generator): yields test client
        test_admin_schema (schema.CreateUser): admin data
    """
    user = test_admin_schema
    user = jsonable_encoder(user)
    response = client.post("/users/", json = user)
    assert response.status_code == 200
    assert response.json()['message'] == "user is a superuser. Automatic account activation."


def test_create_user_email_not_valid(client):
    """Trying:
        post("/users/") using login that is not in email format (and user not an admin)

    Expecting: 
        status code: 405 (Method Not Allowed)
        
        raises an exception with detail: "Login is not a valid email address."

    Args:
        client (Generator): yields test client
    """
    user = schemas.CreateUser(login="fake@", first_name="Arnold",
                            last_name="Tester", address="Westworld",
                            is_admin=False, hashed_password="admin123")
    user = jsonable_encoder(user)
    response = client.post("/users/", json = user)
    assert response.status_code == 405
    assert response.json() == {"detail": "Login is not a valid email address."}


def test_login(client, test_user):
    """Trying:
        post("/token") with valid credentials

    Expecting: 
        status code: 200 (OK)
        
        token exists

        returns token

    Args:
        client (Generator): yields test client
        test_user (schema.CreateUser): user credentials
    """
    response = client.post("/token", data = test_user)
    assert response.status_code == 200
    token = response.json()["access_token"]
    assert token is not None
    return token


def test_login_invalid_credentials(client):
    """Trying:
        post("/token") with invalid credentials

    Expecting: 
        status code: 401 (Unauthorized)
        
        raises an exception with detail: "Incorrect login or password"

    Args:
        client (Generator): yields test client
    """
    response = client.post("/token", data = {"username": "fake_login", "password": "fake_password"})
    assert response.status_code == 401
    assert response.json() == {"detail": "Incorrect login or password"}


def test_read_my_info_not_active(client, test_user):
    """Trying:
        get("/user/me") as inactive user

    Expecting: 
        status code: 401 (Unauthorized)
        
        raises an exception with detail: "Inactive user"

    Args:
        client (Generator): yields test client
        test_user (schema.CreateUser): user credentials
    """
    token = test_login(client, test_user)
    response = client.get("/users/me/", headers={"Authorization": f"Bearer {token}"})
    assert response.status_code == 401
    assert response.json() == {"detail": "Inactive user"}


def test_get_all_rides_user_not_active(client, test_user):
    token = test_login(client, test_user)
    response = client.get("/rides/", headers={"Authorization": f"Bearer {token}"})
    assert response.status_code == 401
    assert response.json() == {'detail':'Inactive user'}


def test_get_all_rides_by_starting_city_user_not_active(client, test_user):
    token = test_login(client, test_user)
    response = client.get("/rides/city_1/", headers={"Authorization": f"Bearer {token}"})
    assert response.status_code == 401
    assert response.json() == {'detail':'Inactive user'}


def test_get_all_rides_by_destination_city_not_an_adm(client, test_user):
    token = test_login(client, test_user)
    response = client.get("/rides/all/city_1/", headers={"Authorization": f"Bearer {token}"})
    assert response.status_code == 401
    assert response.json() == {'detail':'Inactive user'}


def test_get_all_rides_from_one_city_to_another_user_not_active(client, test_user):
    token = test_login(client, test_user)
    response = client.get("/rides/city_1/city_2", headers={"Authorization": f"Bearer {token}"})
    assert response.status_code == 401
    assert response.json() == {'detail':'Inactive user'}


def test_reserve_ride_user_not_active(client, test_user):
    token = test_login(client, test_user)
    response = client.post("/rides/1/reserve", headers={"Authorization": f"Bearer {token}"})
    assert response.status_code == 401
    assert response.json() == {'detail':'Inactive user'}


def test_send_activation_code(client, test_user):
    token = test_login(client, test_user)
    response = client.get("/users/me/send-activation-code", headers={"Authorization": f"Bearer {token}"})
    assert response.status_code == 200
    assert response.json()['message'] == f"activation code has been sent to {test_user['username']}"


def test_send_activation_code_not_logged_in(client):
    response = client.get("/users/me/send-activation-code")
    assert response.status_code == 401


def test_activate_my_account_incorrect_code(client, test_user):
    token = test_login(client, test_user)
    response = client.get(f"/users/1/activate/fake-code",
                          headers={"Authorization": f"Bearer {token}"})
    assert response.status_code == 401
    assert response.json() == {"detail": "Incorrect activation code."}


def test_activate_user(client, test_admin, test_user):
    token = test_login(client, test_admin)
    response = client.patch(f"/users/{test_user['username']}/activate", headers={"Authorization": f"Bearer {token}"})
    assert response.status_code == 200
    assert test_user['username'] == response.json()['login']


def test_send_activation_code_already_active(client, test_user):
    token = test_login(client, test_user)
    response = client.get("/users/me/send-activation-code", headers={"Authorization": f"Bearer {token}"})
    assert response.status_code == 405
    assert response.json() == {"detail": "User already active"}


def test_read_my_info(client, test_user):
    token = test_login(client, test_user)
    response = client.get("/users/me/", headers={"Authorization": f"Bearer {token}"})
    assert response.status_code == 200
    assert test_user['username'] == response.json()['login']


def test_view_user_info_not_an_admin(client, test_user):
    token = test_login(client, test_user)
    response = client.get(f"/users/{test_user['username']}", headers={"Authorization": f"Bearer {token}"})
    assert response.status_code == 401


def test_view_user_info(client, test_admin):
    token = test_login(client, test_admin)
    response = client.get(f"/users/{test_admin['username']}", headers={"Authorization": f"Bearer {token}"})
    assert response.status_code == 200
    assert test_admin['username'] == response.json()['login']


def test_view_user_info_no_user(client, test_admin):
    token = test_login(client, test_admin)
    response = client.get("/users/totally-fake-login", headers={"Authorization": f"Bearer {token}"})
    assert response.status_code == 405
    assert response.json() == {"detail": "There's no user with email = totally-fake-login"}


def test_remove_adm_not_an_admin(client, test_user):
    token = test_login(client, test_user)
    response = client.patch(f"/users/{test_user['username']}/remove-adm", headers={"Authorization": f"Bearer {token}"})
    assert response.status_code == 401 


def test_remove_adm_no_user(client, test_admin):
    token = test_login(client, test_admin)
    response = client.patch(f"/users/totally-fake-login/remove-adm", headers={"Authorization": f"Bearer {token}"})
    assert response.status_code == 405
    assert response.json() == {"detail": "There's no user with email = totally-fake-login"}


def test_remove_adm_user_not_an_admin(client, test_admin, test_user):
    token = test_login(client, test_admin)
    response = client.patch(f"/users/{test_user['username']}/remove-adm", headers={"Authorization": f"Bearer {token}"})
    assert response.status_code == 405 
    assert response.json() == {"detail": "User not an admin"}


def test_grant_adm_no_user(client, test_admin):
    token = test_login(client, test_admin)
    response = client.patch("/users/totally-fake-login/grant-adm", headers={"Authorization": f"Bearer {token}"})
    assert response.status_code == 405
    assert response.json() == {"detail": "There's no user with email = totally-fake-login"}


def test_grant_adm_not_an_admin(client, test_user):
    token = test_login(client, test_user)
    response = client.patch(f"/users/{test_user['username']}/grant-adm", headers={"Authorization": f"Bearer {token}"})
    assert response.status_code == 401 


def test_grant_adm(client, test_admin, test_user):
    token = test_login(client, test_admin)
    response = client.patch(f"/users/{test_user['username']}/grant-adm", headers={"Authorization": f"Bearer {token}"})
    assert response.status_code == 200
    assert test_user['username'] == response.json()['login']
    

def test_grant_adm_user_already_an_admin(client, test_admin, test_user):
    token = test_login(client, test_admin)
    response = client.patch(f"/users/{test_user['username']}/grant-adm", headers={"Authorization": f"Bearer {token}"})
    assert response.status_code == 405 
    assert response.json() == {"detail": "User already an admin"}


def test_remove_adm(client, test_admin, test_user):
    token = test_login(client, test_admin)
    response = client.patch(f"/users/{test_user['username']}/remove-adm", headers={"Authorization": f"Bearer {token}"})
    assert response.status_code == 200 
    assert test_user['username'] == response.json()['login']


def test_get_all_rides_no_rides(client, test_user):
    token = test_login(client, test_user)
    response = client.get("/rides/", headers={"Authorization": f"Bearer {token}"})
    assert response.status_code == 200
    assert response.json() == []


def test_create_ride(client, test_admin, test_ride_1_schema):
    token = test_login(client, test_admin)
    ride = test_ride_1_schema
    ride = jsonable_encoder(ride)
    response = client.post("/rides/", json = ride, headers={"Authorization": f"Bearer {token}"})
    assert response.status_code == 200
    assert response.json()['start_city'] == "city_1"


def test_get_all_rides(client, test_user):
    token = test_login(client, test_user)
    response = client.get("/rides/", headers={"Authorization": f"Bearer {token}"})
    assert response.status_code == 200
    assert len(response.json())


def test_get_all_rides_by_starting_city(client, test_user):
    token = test_login(client, test_user)
    response = client.get("/rides/city_1", headers={"Authorization": f"Bearer {token}"})
    assert response.status_code == 200
    assert len(response.json())


def test_get_all_rides_by_destination_city(client, test_user):
    token = test_login(client, test_user)
    response = client.get("/rides/all/city_2", headers={"Authorization": f"Bearer {token}"})
    assert response.status_code == 200
    assert len(response.json())


def test_get_all_rides_from_one_city_to_another(client, test_user):
    token = test_login(client, test_user)
    response = client.get("/rides/city_1/city_2", headers={"Authorization": f"Bearer {token}"})
    assert response.status_code == 200
    assert len(response.json())


def test_reserve_ride_no_ride(client, test_user):
    token = test_login(client, test_user)
    response = client.post("/rides/5/reserve", headers={"Authorization": f"Bearer {token}"})
    assert response.status_code == 400
    assert response.json() == {"detail":"Can't find any ride with id = 5."}


def test_reserve_ride(client, test_user):
    token = test_login(client, test_user)
    response = client.post("/rides/1/reserve", headers={"Authorization": f"Bearer {token}"})
    assert response.status_code == 200
    assert response.json()['message'] == f"The ride was booked successfully and a detailed email has been sent to {test_user['username']}"


def test_reserve_ride_inactive_ride(client, test_user):
    token = test_login(client, test_user)
    response = client.post("/rides/1/reserve", headers={"Authorization": f"Bearer {token}"})
    assert response.status_code == 405
    assert response.json() == {"detail":"The ride is no longer active."}


def test_create_ride_2(client, test_admin, test_ride_2_schema):
    token = test_login(client, test_admin)
    ride = test_ride_2_schema
    ride = jsonable_encoder(ride)
    response = client.post("/rides/", json = ride, headers={"Authorization": f"Bearer {token}"})
    assert response.status_code == 200
    assert response.json()['start_city'] == "city_2"


def test_archivise_ride_no_ride(client, test_admin):
    token = test_login(client, test_admin)
    response = client.patch("/rides/5/archivise", headers={"Authorization": f"Bearer {token}"})
    assert response.status_code == 400
    assert response.json() == {"detail":"couldn't find a ride with id = 5"}


def test_archivise_ride(client, test_admin):
    token = test_login(client, test_admin)
    response = client.patch("/rides/2/archivise", headers={"Authorization": f"Bearer {token}"})
    assert response.status_code == 200
    assert response.json()['start_city'] == "city_2"


def test_archivise_ride_ride_already_inactive(client, test_admin):
    token = test_login(client, test_admin)
    response = client.patch("/rides/1/archivise", headers={"Authorization": f"Bearer {token}"})
    assert response.status_code == 405
    assert response.json() == {"detail":"ride already deactivated."}


def test_delete_ride(client, test_admin):
    token = test_login(client, test_admin)
    response = client.delete("/rides/1/delete", headers={"Authorization": f"Bearer {token}"})
    assert response.status_code == 200
    assert response.json()['message'] == "ride with id = 1 successfully deleted."


def test_delete_ride_no_ride(client, test_admin):
    token = test_login(client, test_admin)
    response = client.delete("/rides/1/delete", headers={"Authorization": f"Bearer {token}"})
    assert response.status_code == 400
    assert response.json() == {"detail":"couldn't find a ride with id = 1."}


def test_get_all_rides_by_starting_city_no_rides(client, test_user):
    token = test_login(client, test_user)
    response = client.get("/rides/test-city/", headers={"Authorization": f"Bearer {token}"})
    assert response.status_code == 200
    assert response.json() == []


def test_get_all_rides_by_destination_city_no_rides(client, test_user):
    token = test_login(client, test_user)
    response = client.get("/rides/all/test-city", headers={"Authorization": f"Bearer {token}"})
    assert response.status_code == 200
    assert response.json() == []


def test_get_all_rides_from_one_city_to_another_no_rides(client, test_user):
    token = test_login(client, test_user)
    response = client.get("/rides/test-city/test-town", headers={"Authorization": f"Bearer {token}"})
    assert response.status_code == 200
    assert response.json() == []


def test_create_ride_not_an_adm(client, test_user):
    token = test_login(client, test_user)
    response = client.post("/rides/", headers={"Authorization": f"Bearer {token}"})
    assert response.status_code == 401

def test_archivise_ride_not_an_adm(client, test_user):
    token = test_login(client, test_user)
    response = client.patch("/rides/1/archivise", headers={"Authorization": f"Bearer {token}"})
    assert response.status_code == 401


def test_delete_ride_not_an_adm(client, test_user):
    token = test_login(client, test_user)
    response = client.delete("/rides/1/delete", headers={"Authorization": f"Bearer {token}"})
    assert response.status_code == 401

def test_deactivate_user_not_an_admin(client, test_user):
    token = test_login(client, test_user)
    response = client.patch(f"/users/{test_user['username']}/deactivate", headers={"Authorization": f"Bearer {token}"})
    assert response.status_code == 401


def test_deactivate_user_no_user(client, test_admin):
    token = test_login(client, test_admin)
    response = client.patch("/users/totally-fake-login/deactivate", headers={"Authorization": f"Bearer {token}"})
    assert response.status_code == 405
    assert response.json() == {"detail": f"There's no user with email = totally-fake-login"}


def test_deactivate_user(client, test_admin, test_user):
    token = test_login(client, test_admin)
    response = client.patch(f"/users/{test_user['username']}/deactivate", headers={"Authorization": f"Bearer {token}"})
    assert response.status_code == 200
    assert test_user['username'] == response.json()['login']


def test_deactivate_user_user_already_inactive(client, test_admin, test_user):
    token = test_login(client, test_admin)
    response = client.patch(f"/users/{test_user['username']}/deactivate", headers={"Authorization": f"Bearer {token}"})
    assert response.status_code == 405
    assert response.json() == {"detail": "User already inactive"}


def test_activate_user_again(client, test_admin, test_user):
    token = test_login(client, test_admin)
    response = client.patch(f"/users/{test_user['username']}/activate", headers={"Authorization": f"Bearer {token}"})
    assert response.status_code == 200
    assert test_user['username'] == response.json()['login']


def test_activate_user_not_an_admin(client, test_user):
    token = test_login(client, test_user)
    response = client.patch(f"/users/{test_user['username']}/activate", headers={"Authorization": f"Bearer {token}"})
    assert response.status_code == 401


def test_activate_user_no_user(client, test_admin):
    token = test_login(client, test_admin)
    response = client.patch("/users/totally-fake-login/activate", headers={"Authorization": f"Bearer {token}"})
    assert response.status_code == 405
    assert response.json() == {"detail": "There's no user with email = totally-fake-login"}


def test_activate_user_user_already_active(client, test_admin, test_user):
    token = test_login(client, test_admin)
    response = client.patch(f"/users/{test_user['username']}/activate", headers={"Authorization": f"Bearer {token}"})
    assert response.status_code == 405
    assert response.json() == {"detail": "User already active"}


def test_delete_user_not_an_admin(client, test_user):
    token = test_login(client, test_user)
    response = client.patch(f"/users/{test_user['username']}/activate", headers={"Authorization": f"Bearer {token}"})
    assert response.status_code == 401


def test_delete_user(client, test_admin, test_user):
    token = test_login(client, test_admin)
    response = client.delete(f"/users/{test_user['username']}/delete", headers={"Authorization": f"Bearer {token}"})
    assert response.status_code == 200
    assert response.json()['message'] == f"user has been deleted. An email has been sent to the {test_user['username']}."


def test_delete_user_no_user(client, test_admin, test_user):
    token = test_login(client, test_admin)
    response = client.delete(f"/users/{test_user['username']}/delete", headers={"Authorization": f"Bearer {token}"})
    assert response.status_code == 405
    assert response.json() == {"detail": f"There's no user with email = {test_user['username']}"}


def test_delete_my_account(client, test_user, test_user_schema):
    test_create_user(client, test_user_schema)
    token = test_login(client, test_user)
    response = client.delete(f"/users/me/delete", headers={"Authorization": f"Bearer {token}"})
    assert response.status_code == 200
    assert response.json()['message'] == f"Your account has been deleted. An email has been sent to the {test_user['username']}."


def test_delete_my_account_admin(client, test_admin):
    token = test_login(client, test_admin)
    response = client.delete(f"/users/me/delete", headers={"Authorization": f"Bearer {token}"})
    assert response.status_code == 200
    assert response.json()['message'] == "Your account has been deleted."