import pytest
from fastapi import HTTPException
from fastapi.testclient import TestClient
from fastapi.encoders import jsonable_encoder
from app.main import app
from app import schemas, dependencies
from app.database import Base, engine_tests


Base.metadata.create_all(bind=engine_tests)


app.dependency_overrides[dependencies.get_db] = dependencies.override_get_db


client = TestClient(app)


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