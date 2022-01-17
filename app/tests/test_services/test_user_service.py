import pytest
from httpx import AsyncClient
# import os
# import sys
#
# sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from app.main import app
import app.tests.test_database
from app.tests.test_database import init_models


# @app.on_event("startup")
# async def on_startup():
#     await init_models()


@pytest.mark.anyio
async def test_create_new_user():
    json = {
        "username": "test",
        "email": "test@xyz.com",
        "first_name": "test",
        "last_name": "test",
        "password": "test"
    }
    async with AsyncClient(app=app, base_url="http://localhost:8000") as ac:
        response = await ac.post("/user/", json=json)
    print(response.url)
    assert response.status_code == 200
    assert response.json() == {
        "status": 201,
        "transaction": "Successful"
    }
