from fastapi import APIRouter, Depends, status
from fastapi.security import OAuth2PasswordRequestForm, OAuth2PasswordBearer
from passlib.context import CryptContext
from sqlalchemy.ext.asyncio import AsyncSession
from app.core.db_utils import get_db
from app.crud.crud_user import create_user, get_user, get_user_by_username_or_email
from app.schemas.user_details import CreateUser, LoginUser
from datetime import timedelta, datetime
from typing import Optional
from jose import jwt, JWTError
from app.api.responses import success_response, token_exception, get_user_exception, user_exists_exception

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

bcrypt_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# dependency which is going to extract any data from authorization header
oauth2_bearer = OAuth2PasswordBearer(tokenUrl="token")


def get_hashed_password(password):
    return bcrypt_context.hash(password)


def verify_password(plain_password, hashed_password):
    return bcrypt_context.verify(plain_password, hashed_password)


async def authenticate_user(username: str, password: str, db):
    user = await get_user(username, db)
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


async def get_current_user(token: str = Depends(oauth2_bearer)):
    try:
        print(f'token is {token}')
        # if token is None:
        #     raise get_user_exception()
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        user_id: int = payload.get("id")
        if user_id is None or username is None:
            raise get_user_exception()
        return {
            "username": username,
            "id": user_id
        }
    except JWTError:
        raise get_user_exception()


# register
@router.post("/", status_code=status.HTTP_201_CREATED)
async def create_new_user(user_data: CreateUser, db: AsyncSession = Depends(get_db)):
    create_new_user_model = user_info.Users(
        username=user_data.username,
        email=user_data.email,
        first_name=user_data.first_name,
        last_name=user_data.last_name,
        hashed_password=get_hashed_password(user_data.password)
    )

    existing_user = await get_user_by_username_or_email(create_new_user_model, db)

    if existing_user is not None:
        raise user_exists_exception()

    await create_user(create_new_user_model, db)

    return user_data


# login
@router.post("/token")
async def login_for_access_token(login_user_data: LoginUser, db: AsyncSession = Depends(get_db)):
    user = await authenticate_user(login_user_data.username, login_user_data.password, db)
    if not user:
        raise token_exception()
    token_expires = timedelta(minutes=20)
    token = create_access_token(user.username, user.id, expires_delta=token_expires)
    return {
        "token": token
    }
