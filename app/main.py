from contextlib import asynccontextmanager

from fastapi import FastAPI
import rich

from app.database.session import create_all_table

from app.api.router import master_router

from scalar_fastapi import get_scalar_api_reference


@asynccontextmanager
async def lifespan_handler(app: FastAPI):
    rich.print(rich.panel.Panel("Starting up...", border_style="green"))
    await create_all_table()
    yield
    rich.print(rich.panel.Panel("Shutting down...", border_style="red"))


app = FastAPI(lifespan=lifespan_handler)


@app.get("/scalar")
def get_scalar_docs():
    return get_scalar_api_reference(openapi_url=app.openapi_url, title="Scalar API")


app.include_router(master_router)
