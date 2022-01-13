# from sqlalchemy.orm import Session
from sqlalchemy.ext.asyncio import AsyncSession


async def create_user(create_new_user_model, db: AsyncSession):
    db.add(create_new_user_model)
    await db.commit()
    return True
# sqlalchemy/ext/asyncio/session.py
