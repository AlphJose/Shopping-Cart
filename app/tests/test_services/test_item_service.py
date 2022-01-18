from typing import List

import pytest
from httpx import AsyncClient
from app.main import app
from app.tests.conftest import init_models


@pytest.mark.asyncio
async def test_create_new_item():
    json = {
        "item_name": "test_item",
        "price": "100"
    }
    async with AsyncClient(app=app, base_url="http://localhost:8000") as ac:
        response = await ac.post("/item/", json=json)
    print(response.url)
    assert response.status_code == 200
    assert response.json() == {
        "status": 201,
        "transaction": "Successful"
    }


@pytest.mark.asyncio
async def test_get_items_list(create_and_get_items: List[str]):
    json = {
        "item_name": "test_item",
        "price": "100"
    }

    async with AsyncClient(app=app, base_url="http://localhost:8000") as ac:
        response = await ac.get("/item/")
    print(response.json())
    assert response.status_code == 200
    assert json in response.json()
