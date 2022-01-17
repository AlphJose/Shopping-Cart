from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.responses import success_response
from app.core.db_utils import get_db
from app.models import item_info
from app.crud.crud_item import get_items, create_item
from app.schemas.item_details import CreateItem

router = APIRouter(
    prefix="/item",
    tags=["item"],
    responses={
        401: {
            "user": "Not authorized"
        }
    }
)


# get list of items for user
@router.get("/")
async def get_items_list(db: AsyncSession = Depends(get_db)):
    items_list = {}
    items_list = await get_items(db)
    return items_list


# create item for admin
@router.post("/")
async def create_new_item(item_data: CreateItem, db: AsyncSession = Depends(get_db)):
    create_new_item_model = item_info.Items()
    create_new_item_model.item_name = item_data.item_name
    create_new_item_model.price = item_data.price

    await create_item(create_new_item_model, db)

    return success_response(201)
