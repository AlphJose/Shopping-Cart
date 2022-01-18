from sqlalchemy import select
from app.models import item_info


async def get_items(db):
    query = select(item_info.Items)
    result = await db.execute(query)
    curr = result.fetchall()
    # TODO: put a cap on number of rows returned. for eg: return first 25 records
    return curr


async def create_item(create_new_item_model, db):
    print("adding item data")
    print(db)
    db.add(create_new_item_model)
    await db.commit()
