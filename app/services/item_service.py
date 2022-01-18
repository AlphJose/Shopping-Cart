from fastapi import APIRouter, Depends, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.responses import item_exists_exception, get_user_exception, admin_access_exception
from app.core.db_utils import get_db
from app.crud.crud_user import get_all_users
from app.models import item_info
from app.crud.crud_item import get_items, create_item, get_item_by_item_name
from app.schemas.item_details import CreateItem
from app.services.user_service import get_current_user

router = APIRouter(
    prefix="/item",
    tags=["item"],
    responses={
        401: {
            "user": "Not authorized"
        }
    }
)


# create item for admin
@router.post("/", status_code=status.HTTP_201_CREATED)
async def create_new_item(item_data: CreateItem,
                          user: dict = Depends(get_current_user),
                          db: AsyncSession = Depends(get_db)):
    print(user)
    await get_all_users(db)
    if user is None:
        raise get_user_exception()
    if user.get("username") != "admin":
        raise admin_access_exception()
    else:
        create_new_item_model = item_info.Items()
        create_new_item_model.item_name = item_data.item_name
        create_new_item_model.price = item_data.price

        existing_item = await get_item_by_item_name(item_data.item_name, db)

        if existing_item is not None:
            raise item_exists_exception()

        await create_item(create_new_item_model, db)

        return item_data


# get list of items for user
@router.get("/")
async def get_items_list(db: AsyncSession = Depends(get_db)):
    items_list = await get_items(db)
    return items_list
