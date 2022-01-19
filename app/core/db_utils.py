from sqlalchemy.exc import DBAPIError, SQLAlchemyError
from sqlalchemy.ext.asyncio import create_async_engine

from app.core.database import SessionLocal

from app.core.database import engine, Base


async def init_models():
    async with engine.begin() as conn:
        # await conn.run_sync(Base.metadata.drop_all)
        await conn.run_sync(Base.metadata.create_all)


""""
Dropping and creating tables from Base.metadata doesn't run async by default
and there is generally no reason for us to call it within an async function.
This is just an example that shows how SQLAlchemy can run otherwise sync operations with run_sync().
"""


async def get_db():
    try:
        async with SessionLocal() as db:
            yield db
    finally:
        await db.close()

SQLALCHEMY_DATABASE_URL = "sqlite+aiosqlite:///./shoppingcartapp"


def get_db_engine():
    test_engine = create_async_engine(
        SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False}
    )
    return test_engine


async def create_database():
    status = True, ""

    try:
        test_engine = get_db_engine()

        # Base.metadata.create_all(test_engine, checkfirst=False)
        async with test_engine.begin() as conn:
            await conn.run_sync(Base.metadata.drop_all)
            await conn.run_sync(Base.metadata.create_all)
    except (DBAPIError, SQLAlchemyError) as exc:
        status = False, str(exc)

    return status


async def remove_database():
    status = True, ""

    try:
        test_engine = get_db_engine()
        async with test_engine.begin() as conn:
            await conn.run_sync(Base.metadata.drop_all)
    except DBAPIError as exc:
        status = False, str(exc)

    return status
