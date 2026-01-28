from contextlib import asynccontextmanager

from fastapi import FastAPI
import rich

from app.database.session import create_all_table

from app.api.router import master_router


@asynccontextmanager
async def lifespan_handler(app: FastAPI):
    rich.print(rich.panel.Panel("Starting up...", border_style="green"))
    await create_all_table()
    yield
    rich.print(rich.panel.Panel("Shutting down...", border_style="red"))


app = FastAPI(lifespan=lifespan_handler)

app.include_router(master_router)
