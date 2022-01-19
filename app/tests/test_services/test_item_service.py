import pytest
from httpx import AsyncClient
from fastapi import status

from app.core import db_utils
from app.core.database import get_db_session
from app.crud.crud_item import create_item
from app.main import app
from app.models import item_info
from app.services.item_service import create_new_item
from app.tests.conftest import DB_NAME


async def setup_db_with_info():
    await db_utils.remove_database()
    await db_utils.create_database()
    async with get_db_session() as db_session:
        item_details = item_info.Items(item_name="test_item", price=100)
        await create_item(item_details, db_session)


@pytest.mark.asyncio
async def test_get_items_list(client: AsyncClient):
    json = {
        "item_name": "test_item",
        "price": 100.0
    }

    await setup_db_with_info()
    print("setup done")
    response = await client.get(
        "/item/",
    )
    assert response.status_code == status.HTTP_200_OK
    # assert json in response.json()
    print(response.json()[0]['Items'])
    assert response.json()[0]['Items']['item_name'] == json['item_name']
    assert response.json()[0]['Items']['price'] == json['price']
    await db_utils.remove_database()


@pytest.mark.asyncio
async def test_create_new_item(client: AsyncClient, get_token_for_test_admin):
    await db_utils.remove_database()

    json = {
        "item_name": "test_item_create",
        "price": 100
    }
    await setup_db_with_info()

    # TODO: authorized as admin required
    # value = f'Bearer {get_token_for_test_admin}'
    # headers = {
    #     'Authorization': value
    # }
    headers = {
        'Authorization': 'Bearer {}'.format(get_token_for_test_admin),
    }

    async with AsyncClient(app=app, base_url="http://localhost:8000", headers=headers) as client:
        response = await client.post("/item/", json=json)
    print(response.url)
    print(response.json())
    assert response.status_code == 201
    assert response.json() == json
