from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker
from app.core.database import Base
from app.main import app
from app.core.db_utils import get_db

SQLALCHEMY_DATABASE_URL = "sqlite+aiosqlite:///./shoppingcartapp"

engine = create_async_engine(
    SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False}
)
#
# engine = create_async_engine(
#     SQLALCHEMY_DATABASE_URL,
#     echo=True
# )
# engine = create_async_engine(
#         "sqlite+aiosqlite:///:memory:",
#         echo=True,
#     )

TestingSessionLocal = sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)


# Base.metadata.create_all(bind=test_engine)
async def init_models():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)
        await conn.run_sync(Base.metadata.create_all)


def override_get_db():
    try:
        db = TestingSessionLocal()
        yield db
    finally:
        db.close()


app.dependency_overrides[get_db] = override_get_db
