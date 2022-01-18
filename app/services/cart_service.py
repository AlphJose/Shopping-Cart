from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.responses import success_response
from app.core.db_utils import get_db
from app.crud.crud_cart import show_cart_items, create_cart, remove_cart, remove_cart_of_owner
from app.models import cart_info
from app.schemas.cart_details import CreateCart
from app.services.user_service import get_current_user, get_user_exception

router = APIRouter(
    prefix="/cart",
    tags=["cart"],
    responses={
        401: {
            "user": "Not authorized"
        }
    }
)


@router.post("/")
async def create_new_cart(cart_data: CreateCart, user: dict = Depends(get_current_user),
                          db: AsyncSession = Depends(get_db)):
    owner_id = user.get("id")
    create_new_cart_model = cart_info.Carts(
        owner_id=owner_id,
        item_id=cart_data.item_id
    )

    await create_cart(create_new_cart_model, db)

    # return success_response(201)
    return cart_data


# get list of items in a cart
@router.get("/")
async def show_user_cart(user: dict = Depends(get_current_user), db: AsyncSession = Depends(get_db)):
    if user is None:
        raise get_user_exception()
    else:
        owner_id = user.get("id")
        cart = await show_cart_items(db, owner_id=owner_id)
        return cart


@router.delete("/{cart_id}")
async def delete_cart(cart_id: int,
                      user: dict = Depends(get_current_user),
                      db: AsyncSession = Depends(get_db)):
    if user is None:
        raise get_user_exception()

    await remove_cart(cart_id, db)

    return success_response(204)


@router.post("/checkout/")
async def checkout_user_carts(user: dict = Depends(get_current_user),
                              db: AsyncSession = Depends(get_db)):
    if user is None:
        raise get_user_exception()
    owner_id = user.get("id")
    await remove_cart_of_owner(owner_id=owner_id, db=db)
    return success_response(200)
