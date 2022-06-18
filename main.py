from fastapi import FastAPI

from db import init_db, close_db
from routes import router


app = FastAPI()
app.include_router(router)


@app.on_event('startup')
async def startup():
    await init_db()


@app.on_event('shutdown')
async def shutdown():
    await close_db()
