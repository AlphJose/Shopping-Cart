from fastapi import FastAPI
from app.services import user_service
from app.models import user_info
from app.core.database import engine

app = FastAPI()

user_info.Base.metadata.create_all(bind=engine)

app.include_router(user_service.router)


@app.get("/")
async def test():
    return {"response": "Successful test"}
