import pytest
from httpx import AsyncClient

from app.core import db_utils


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
    response = await client.post("/user/", json=json)
    assert response.status_code == 201
    assert response.json() == json


@pytest.mark.asyncio
async def test_login_for_access_token(client: AsyncClient):
    await setup_db_with_info()
    json1 = {
        "username": "test",
        "password": "test"
    }
    response = await client.post("/user/token/", json=json1)
    assert response.status_code == 200 or response.status_code == 307
