import pytest
from fastapi.testclient import TestClient
from app.main import app
from app import schemas
from app.utils import Envs


@pytest.fixture(scope="module")
def client():
    """Test fixture for the module yielding a test client

    Yields:
        TestClient: test client
    """
    with TestClient(app) as c:
      yield c


@pytest.fixture(scope="module")
def test_user_schema() -> schemas.CreateUser:
    """Test fixture for the module returning create schema for test user

    Returns:
        schemas.CreateUser: user data on user creation
    """
    return schemas.CreateUser(login=Envs.TEST_MAIL, first_name="John",
                        last_name="Tester", address="Cyberworld",
                        is_admin=False, hashed_password="admin123")


@pytest.fixture(scope="module")
def test_admin_schema() -> schemas.CreateUser:
    """Test fixture for the module returning create schema for test admin

    Returns:
        schemas.CreateUser: user data on user creation
    """
    return schemas.CreateUser(login="fake_admin", first_name="Victor",
                        last_name="Tester", address="Cyberworld",
                        is_admin=True, hashed_password="admin123")


@pytest.fixture(scope="module")
def test_ride_1_schema() -> schemas.RideCreate:
    """Test fixture for the module returning create schema for test ride no. 1

    Returns:
        schemas.RideCreate: ride data on ride creation
    """
    return schemas.RideCreate(start_city = "city_1", destination_city = "city_2",
                           distance = 1, km_fee= 1, departure_date="2020-01-01 19:30")


@pytest.fixture(scope="module")
def test_ride_2_schema():
    """Test fixture for the module returning create schema for test ride no. 2

    Returns:
        schemas.RideCreate: ride data on ride creation
    """
    return schemas.RideCreate(start_city = "city_2", destination_city = "city_1",
                        distance = 1, km_fee= 1, departure_date="2020-01-01 19:30")


@pytest.fixture(scope="module")
def test_user() -> dict:
    """Test fixture for the module returning user data used for logging in

    Returns:
        dict: username and password
    """
    return {"username": Envs.TEST_MAIL, "password": "admin123"}


@pytest.fixture(scope="module")
def test_admin() -> dict:
    """Test fixture for the module returning admin data used for logging in

    Returns:
        dict: username and password
    """
    return {"username": "fake_admin", "password": "admin123"}