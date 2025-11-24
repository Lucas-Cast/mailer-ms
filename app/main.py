from typing import Union

from fastapi import FastAPI
from fastapi.concurrency import asynccontextmanager

from app.core.db import create_tables, shutdown_engine
from app.core.seeds import run_seeds


@asynccontextmanager
async def lifespan(app: FastAPI):
    await create_tables()
    await run_seeds()

    yield

    await shutdown_engine()


app = FastAPI(lifespan=lifespan)


@app.get("/")
async def read_root():
    return {"Hello": "World"}


@app.get("/items/{item_id}")
async def read_item(item_id: int, q: Union[str, None] = None):
    return {"item_id": item_id, "q": q}
