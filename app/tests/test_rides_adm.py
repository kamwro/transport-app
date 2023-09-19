import pytest
from fastapi import HTTPException
from fastapi.testclient import TestClient
from fastapi.encoders import jsonable_encoder
from ..main import app
from .. import schemas, dependencies
from ..database import Base, engine_tests


Base.metadata.create_all(bind=engine_tests)


app.dependency_overrides[dependencies.get_db] = dependencies.override_get_db


client = TestClient(app)


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