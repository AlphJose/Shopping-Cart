from fastapi import FastAPI
from app.core.db_utils import init_models
from app.services import user_service, item_service, cart_service

app = FastAPI()


@app.on_event("startup")
async def on_startup():
    await init_models()


app.include_router(user_service.router)
app.include_router(item_service.router)
app.include_router(cart_service.router)
