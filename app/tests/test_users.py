from fastapi.testclient import TestClient
from fastapi.encoders import jsonable_encoder
from ..routers.users import router
from .. import schemas

client = TestClient(router)

# def test_create_user_not_superuser():
#     response = client.post("/", json = {})
#     assert response.status_code == 200
#     assert response.json() == {"user data: ": [user_data], "message": f"activation code has been sent to {new_user.login}"}