from sqlalchemy import select, delete

from app.api.responses import http_exception
from app.models import cart_info, item_info


# item details of items associated with current user
async def show_cart_items(db, owner_id):
    # query = select(cart_info.Carts, item_info.Items)\
    #     .join(item_info.Items, cart_info.Carts.item_id == item_info.Items.id)\
    #     .where(cart_info.Carts.owner_id == owner_id)
    query = select(cart_info.Carts.item_id, item_info.Items.item_name, item_info.Items.price) \
        .where(cart_info.Carts.item_id == item_info.Items.id and cart_info.Carts.owner_id == owner_id)
    result = await db.execute(query)
    rows = result.fetchall()
    # for cart_item in rows:
    #     item_ids.append(cart_item)
    return rows


async def create_cart(create_new_cart_model, db):
    db.add(create_new_cart_model)
    await db.commit()


async def remove_cart(cart_id, db):
    query = select(cart_info.Carts).where(cart_info.Carts.id == cart_id)

    result = await db.execute(query)
    cart_model = result.scalars().first()

    if cart_model is None:
        raise http_exception()

    await db.delete(cart_model)

    # query = delete(cart_info.Carts).where(cart_info.Carts.id == cart_id)
    # await db.execute(query)
    await db.commit()


async def remove_cart_of_owner(owner_id, db):
    query = select(cart_info.Carts).where(cart_info.Carts.owner_id == owner_id)

    result = await db.execute(query)
    cart_model = result.fetchall()

    if cart_model is None:
        raise http_exception()

    query = delete(cart_info.Carts).where(cart_info.Carts.owner_id == owner_id)
    await db.execute(query)
    await db.commit()
