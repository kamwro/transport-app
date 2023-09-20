import pytest
from fastapi.testclient import TestClient
from app.main import app
from app import schemas
from app.utils import Envs


@pytest.fixture(scope="module")
def client():
    with TestClient(app) as c:
      yield c


@pytest.fixture(scope="module")
def test_user_schema() -> dict:
    return {"with_password": schemas.CreateUser(login=Envs.TEST_MAIL, first_name="John",
                        last_name="Tester", address="Cyberworld",
                        is_admin=False, hashed_password="admin123")
                        ,
            "with_activation_code": schemas.ActivateUser(login=Envs.TEST_MAIL, first_name="John",
                        last_name="Tester", address="Cyberworld",
                        is_admin=False, activation_code="fake_code")}


@pytest.fixture(scope="module")
def test_admin_schema():
    return schemas.CreateUser(login="fake_admin", first_name="Victor",
                        last_name="Tester", address="Cyberworld",
                        is_admin=True, hashed_password="admin123")


@pytest.fixture(scope="module")
def test_ride_1_schema():
    return schemas.RideCreate(start_city = "city_1", destination_city = "city_2",
                           distance = 1, km_fee= 1, departure_date="2020-01-01 19:30")


@pytest.fixture(scope="module")
def test_ride_2_schema():
    return schemas.RideCreate(start_city = "city_2", destination_city = "city_1",
                        distance = 1, km_fee= 1, departure_date="2020-01-01 19:30")


@pytest.fixture(scope="module")
def test_user():
    return {"username": Envs.TEST_MAIL, "password": "admin123"}


@pytest.fixture(scope="module")
def test_admin():
    return {"username": "fake_admin", "password": "admin123"}