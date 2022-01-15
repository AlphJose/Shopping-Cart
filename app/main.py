import asyncio
import typer
from fastapi import FastAPI
# from app.models import user_info, item_info, cart_info
from app.core.db_utils import init_models
from app.services import user_service

app = FastAPI()

cli = typer.Typer()


# @cli.command()
# def db_init_models():
#     print("entered db_init_models")
#     asyncio.run(init_models())
#     print("Done - db_init_models")


@app.on_event("startup")
async def on_startup():
    await init_models()


# if __name__ == "__main__":
#     cli()

app.include_router(user_service.router)


@app.get("/")
async def welcome():
    return {"response": "Please navigate to /docs"}

#
# if __name__ == "__main__":
#     cli()
