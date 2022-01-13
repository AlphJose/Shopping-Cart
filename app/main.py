import asyncio
import typer
from fastapi import FastAPI
from app.core.db_utils import init_models
from app.services import user_service

app = FastAPI()

cli = typer.Typer()


@cli.command()
def db_init_models():
    asyncio.run(init_models())
    print("Done")


if __name__ == "__main__":
    cli()

app.include_router(user_service.router)


@app.get("/")
async def test():
    return {"response": "Successful test"}
