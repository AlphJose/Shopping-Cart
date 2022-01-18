import pytest
from httpx import AsyncClient
from app.main import app


# from app.tests.test_database import init_models


@pytest.mark.asyncio
async def test_create_new_user():
    json = {
        "username": "test_user",
        "email": "test@xyz.com",
        "first_name": "test",
        "last_name": "test",
        "password": "test"
    }
    async with AsyncClient(app=app, base_url="http://localhost:8000") as client:
        response = await client.post("/user/", json=json)
    print(response.url)
    assert response.status_code == 200
    assert response.json() == json


@pytest.mark.asyncio
async def test_login_for_access_token():
    json = {
        "username": "test",
        "password": "test"
    }
    async with AsyncClient(app=app, base_url="http://localhost:8000") as ac:
        response = await ac.post("/user/token/", json=json)
    # print(response.url)
    assert response.status_code == 200 or response.status_code == 307
    # TODO: figure out why 307
    # assert response.json() == {
    #     "status": 201,
    #     "transaction": "Successful"
    # }
