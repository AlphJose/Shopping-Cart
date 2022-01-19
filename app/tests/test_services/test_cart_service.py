import pytest
from httpx import AsyncClient

from app.core import db_utils
from app.core.database import get_db_session
from app.crud.crud_cart import create_cart
from app.crud.crud_item import create_item
from app.main import app
from app.models import item_info, cart_info


async def setup_db_with_info():
    await db_utils.remove_database()
    await db_utils.create_database()
    async with get_db_session() as db_session:
        item_details = item_info.Items(item_name="test_item", price=100)
        await create_item(item_details, db_session)


async def setup_db_with_info_cart():
    await db_utils.remove_database()
    await db_utils.create_database()
    async with get_db_session() as db_session:
        item_details = item_info.Items(item_name="test_item", price=100)
        await create_item(item_details, db_session)
        cart_details = cart_info.Carts(item_id=1, owner_id=1)
        await create_cart(cart_details, db_session)


@pytest.mark.asyncio
async def test_create_new_cart(client: AsyncClient, get_token_for_test):
    await setup_db_with_info()

    json = {
        "item_id": 1
    }

    headers = {
        'Authorization': 'Bearer {}'.format(get_token_for_test),
    }

    async with AsyncClient(app=app, base_url="http://localhost:8000", headers=headers) as client:
        response = await client.post("/cartItem/", json=json)
    print(response.url)
    assert response.status_code == 200
    assert response.json() == json


@pytest.mark.asyncio
async def test_show_user_cart(client: AsyncClient, get_token_for_test):
    await setup_db_with_info_cart()

    headers = {
        'Authorization': 'Bearer {}'.format(get_token_for_test),
    }

    async with AsyncClient(app=app, base_url="http://localhost:8000", headers=headers) as client:
        response = await client.get("/cartItem/")
    print(response.url)
    assert response.status_code == 200
    json = {
        "item_id": 1,
        "item_name": "test_item",
        "unit_price": 100.0,
        "count": 1,
        "total_price_for_item": 100.0
    }
    assert json in response.json()


@pytest.mark.asyncio
async def test_remove_cart_item_for_user(client: AsyncClient, get_token_for_test):
    await setup_db_with_info_cart()

    headers = {
        'Authorization': 'Bearer {}'.format(get_token_for_test),
    }

    async with AsyncClient(app=app, base_url="http://localhost:8000", headers=headers) as client:
        response = await client.post("/cartItem/1")
    print(response.url)
    assert response.status_code == 200


@pytest.mark.asyncio
async def test_checkout_user_carts(client: AsyncClient, get_token_for_test):
    await setup_db_with_info_cart()

    headers = {
        'Authorization': 'Bearer {}'.format(get_token_for_test),
    }

    async with AsyncClient(app=app, base_url="http://localhost:8000", headers=headers) as client:
        response = await client.post("/cartItem/checkout/")
    print(response.url)
    assert response.status_code == 200
