from fastapi import APIRouter, Depends
from passlib.context import CryptContext
from sqlalchemy.ext.asyncio import AsyncSession
from app.core.database import SessionLocal
from app.crud.crud_user import create_user
from app.schemas.user_details import CreateUser

from app.models import user_info, cart_info, item_info
"""
the cart_info, item_info are imported to avoid the following error:

sqlalchemy.exc.InvalidRequestError: When initializing mapper mapped class Users->users, 
expression 'Carts' failed to locate a name ('Carts'). 
If this is a class name, consider adding this relationship() to the <class 'app.models.user_info.Users'> class 
after both dependent classes have been defined.
"""


router = APIRouter(
    prefix="/user",
    tags=["user"],
    responses={
        401: {
            "user": "Not authorized"
        }
    })


async def get_db():
    try:
        async with SessionLocal() as db:
            yield db
    finally:
        await db.close()


bcrypt_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def get_hashed_password(password):
    return bcrypt_context.hash(password)


def success_response(status_code: int):
    return {
        "status": status_code,
        "transaction": "Successful"
    }


@router.post("/create")
async def create_new_user(user_data: CreateUser, db: AsyncSession = Depends(get_db)):
    create_new_user_model = user_info.Users()
    create_new_user_model.username = user_data.username
    create_new_user_model.email = user_data.email
    create_new_user_model.first_name = user_data.first_name
    create_new_user_model.last_name = user_data.last_name
    create_new_user_model.hashed_password = get_hashed_password(user_data.password)

    await create_user(create_new_user_model, db)

    return success_response(201)
