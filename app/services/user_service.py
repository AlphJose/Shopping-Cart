from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from passlib.context import CryptContext
from sqlalchemy.ext.asyncio import AsyncSession
# from app.core.database import SessionLocal
from app.core.db_utils import get_db
from app.crud.crud_user import create_user, get_user
from app.schemas.user_details import CreateUser
from datetime import timedelta, datetime
from typing import Optional
from jose import jwt
from sqlalchemy import select
from app.api.responses import success_response

from app.models import user_info, cart_info, item_info

"""
the cart_info, item_info are imported to avoid the following error:

sqlalchemy.exc.InvalidRequestError: When initializing mapper mapped class Users->users, 
expression 'Carts' failed to locate a name ('Carts'). 
If this is a class name, consider adding this relationship() to the <class 'app.models.user_info.Users'> class 
after both dependent classes have been defined.
"""

SECRET_KEY = "415a6dceac9ef79dae62af8901bb030093b98b3e46e3627e996207e3c7d29375"
ALGORITHM = "HS256"

router = APIRouter(
    prefix="/user",
    tags=["user"],
    responses={
        401: {
            "user": "Not authorized"
        }
    })

# async def get_db():
#     try:
#         async with SessionLocal() as db:
#             yield db
#     finally:
#         await db.close()


bcrypt_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def get_hashed_password(password):
    return bcrypt_context.hash(password)


# register
@router.post("/")
async def create_new_user(user_data: CreateUser, db: AsyncSession = Depends(get_db)):
    create_new_user_model = user_info.Users()
    create_new_user_model.username = user_data.username
    create_new_user_model.email = user_data.email
    create_new_user_model.first_name = user_data.first_name
    create_new_user_model.last_name = user_data.last_name
    create_new_user_model.hashed_password = get_hashed_password(user_data.password)

    await create_user(create_new_user_model, db)

    return success_response(201)


# login
def verify_password(plain_password, hashed_password):
    return bcrypt_context.verify(plain_password, hashed_password)


async def authenticate_user(username: str, password: str, db):
    # user = db.query(user_info.Users).filter(user_info.Users.username == username).first()
    # query = select(user_info.Users).where(user_info.Users.username == username)
    # result = await db.execute(query)
    # user = result.scalars().first()
    user = get_user(username, db)
    if not user:
        return False
    if not verify_password(password, user.hashed_password):
        return False
    return user


def create_access_token(username: str, user_id: int,
                        expires_delta: Optional[timedelta] = None):
    encode = {"sub": username, "id": user_id}
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=15)

    encode.update({"exp": expire})
    return jwt.encode(encode, SECRET_KEY, algorithm=ALGORITHM)


@router.post("/token")
async def login_for_access_token(form_data: OAuth2PasswordRequestForm = Depends(), db: AsyncSession = Depends(get_db)):
    user = await authenticate_user(form_data.username, form_data.password, db)
    if not user:
        raise token_exception()
    token_expires = timedelta(minutes=20)
    token = create_access_token(user.username, user.id, expires_delta=token_expires)
    return {
        "token": token
    }


# Exceptions
def token_exception():
    token_exception_response = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Incorrect username or password",
        headers={"WWW-Authenticate": "Bearer"}
    )
    return token_exception_response
