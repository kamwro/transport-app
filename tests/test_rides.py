import pytest
from fastapi import HTTPException
from fastapi.testclient import TestClient
from fastapi.encoders import jsonable_encoder
from app.main import app
from .. import schemas, dependencies
from app.database import Base, engine_tests


Base.metadata.create_all(bind=engine_tests)


app.dependency_overrides[dependencies.get_db] = dependencies.override_get_db


client = TestClient(app)


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