from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from app.models import user_info


async def create_user(create_new_user_model, db: AsyncSession):
    db.add(create_new_user_model)
    await db.commit()


async def get_user(username: str, db):
    query = select(user_info.Users).where(user_info.Users.username == username)
    result = await db.execute(query)
    user = result.scalars().first()
    return user
