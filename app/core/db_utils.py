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
