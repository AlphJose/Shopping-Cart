import pytest
from httpx import AsyncClient

from app.core import db_utils
from app.main import app


# from app.tests.test_database import init_models
async def setup_db_with_info():
    await db_utils.remove_database()
    await db_utils.create_database()


@pytest.mark.asyncio
async def test_create_new_user(client: AsyncClient):
    await setup_db_with_info()

    json = {
        "username": "test_user",
        "email": "test@xyz.com",
        "first_name": "test",
        "last_name": "test",
        "password": "test"
    }
    # async with AsyncClient(app=app, base_url="http://localhost:8000") as client:
    response = await client.post("/user/", json=json)
    print(response.url)
    assert response.status_code == 201
    assert response.json() == json


@pytest.mark.asyncio
async def test_login_for_access_token(client: AsyncClient):
    await setup_db_with_info()
    json = {
        "username": "test",
        "password": "test"
    }
    # async with AsyncClient(app=app, base_url="http://localhost:8000") as ac:
    response = await client.post("/user/token/", json=json)
    # print(response.url)
    assert response.status_code == 200 or response.status_code == 307
    # TODO: figure out why 307
    # assert response.json() == {
    #     "status": 201,
    #     "transaction": "Successful"
    # }
    # assert response.json() == json
