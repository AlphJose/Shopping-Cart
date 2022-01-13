import asyncio

from fastapi import FastAPI
from app.services import user_service
from app.models import user_info
from app.core.database import engine
from app.services.user_service import init_models

app = FastAPI()


# user_info.Base.metadata.create_all(bind=engine)
def db_init_models():
    asyncio.run(init_models())
    print("Done")


app.include_router(user_service.router)


@app.get("/")
async def test():
    return {"response": "Successful test"}
