from sqlalchemy import select, delete

from app.api.responses import http_exception
from app.models import cart_info, item_info


# item details of items associated with current user
async def show_cart_items(db, owner_id):
    query = f"select items.id as item_id, items.item_name, items.price as unit_price, count(*) as count," \
            " sum(items.price) as total_price_for_item from items " \
            f"inner join carts on (items.id = carts.item_id and carts.owner_id = {owner_id})" \
            " group by carts.item_id"
    result = await db.execute(query)
    rows = result.fetchall()
    return rows


async def create_cart(create_new_cart_model, db):
    db.add(create_new_cart_model)
    await db.commit()


async def remove_cart_item(item_id, db):
    query = select(cart_info.Carts).where(cart_info.Carts.item_id == item_id)

    result = await db.execute(query)
    cart_model = result.scalars().first()

    if cart_model is None:
        raise http_exception()

    await db.delete(cart_model)

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
