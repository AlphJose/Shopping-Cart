import pytest
from httpx import AsyncClient
from app.main import app
from app.services.user_service import get_current_user


def override_get_current_user():
    return {
        "username": "test",
        "id": 1
    }


app.dependency_overrides[get_current_user] = override_get_current_user


@pytest.mark.asyncio
async def test_create_new_cart():
    json = {
        "item_id": 1
    }
    async with AsyncClient(app=app, base_url="http://localhost:8000") as ac:
        response = await ac.post("/cart/", json=json)
    print(response.url)
    assert response.status_code == 200
    assert response.json() == json

# rest of the tests require creating carts as a prerequisite
