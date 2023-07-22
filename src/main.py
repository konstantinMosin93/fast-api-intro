from fastapi import FastAPI

from src.db import close_db
from src.db import init_db
from src.routes import router


app = FastAPI()
app.include_router(router)


@app.on_event('startup')
async def startup() -> None:
    await init_db()


@app.on_event('shutdown')
async def shutdown() -> None:
    await close_db()
