from fastapi.testclient import TestClient
from ..routers.rides import router

client = TestClient(router)