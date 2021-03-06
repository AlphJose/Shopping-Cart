from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, or_
from app.models import user_info


async def create_user(create_new_user_model, db: AsyncSession):
    db.add(create_new_user_model)
    await db.commit()


async def get_user(username: str, db):
    query = select(user_info.Users).where(user_info.Users.username == username)
    result = await db.execute(query)
    user = result.scalars().first()
    return user


async def get_user_by_username_or_email(user_model, db):
    query = select(user_info.Users) \
        .filter(or_(user_info.Users.username == user_model.username, user_info.Users.email == user_model.email))

    result = await db.execute(query)
    user = result.scalars().first()
    return user


async def get_all_users(db):
    query = select(user_info.Users)
    result = await db.execute(query)
    curr = result.fetchall()
    print(curr)
