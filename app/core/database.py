from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine, async_scoped_session
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from contextlib import asynccontextmanager
from asyncio import current_task
import os

SQLALCHEMY_DATABASE_URL = os.getenv("DB_URL")

print("loaded env", SQLALCHEMY_DATABASE_URL)

engine = create_async_engine(
    SQLALCHEMY_DATABASE_URL,
    echo=True
)

Base = declarative_base()

SessionLocal = sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)

"""
We should disable the "expire on commit" behavior of sessions with expire_on_commit=False.
This is because in async settings, we don't want SQLAlchemy to issue new SQL queries to
the database when accessing already committed objects.
"""


@asynccontextmanager
async def get_db_session() -> AsyncSession:
    test_db_engine = await get_db_engine()
    session = async_scoped_session(
        sessionmaker(
            autocommit=False,
            autoflush=True,
            bind=test_db_engine,
            class_=AsyncSession,
        ),
        scopefunc=current_task,
    )
    # session = sessionmaker(test_db_engine, class_=AsyncSession, expire_on_commit=False)

    try:
        yield session
    finally:
        await session.close()


async def get_db_engine():
    sqlite_client_str = "sqlite+aiosqlite:///./shoppingcartapp"
    print(sqlite_client_str)
    test_db_engine = create_async_engine(sqlite_client_str, echo=True)
    return test_db_engine
