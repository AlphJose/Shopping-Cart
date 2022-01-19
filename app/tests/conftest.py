import asyncio
from datetime import timedelta

import pytest
from httpx import AsyncClient

from app.core.database import get_db_session
from app.core.db_utils import get_db
from app.main import app
from app.core import db_utils
from app.services.user_service import create_access_token

TEST_BASE_URL = "http://localhost:8000"
DB_NAME = "shoppingcartapp"


@pytest.fixture
async def client(test_db):
    # app.dependency_overrides[get_db] = get_db_session

    # app.dependency_overrides = {}
    async with AsyncClient(app=app, base_url=TEST_BASE_URL) as client:
        yield client


@pytest.fixture(scope="session")
async def test_db():
    """Create a testing database for the tests session."""

    await db_utils.create_database()
    yield DB_NAME
    await db_utils.remove_database()


@pytest.fixture(scope="session")
def event_loop():
    loop = asyncio.get_event_loop()
    yield loop
    loop.close()


#
# app.dependency_overrides[get_db] = get_db_session

@pytest.fixture()
def get_token_for_test_admin():
    token = create_access_token("admin", 1, timedelta(minutes=60))
    return token


@pytest.fixture()
def get_token_for_test():
    token = create_access_token("test", 1, timedelta(minutes=60))
    return token
