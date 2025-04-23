from contextlib import asynccontextmanager

import uvicorn
from fastapi import FastAPI

from server.api.routers import router
from server.core.models import Base, db_helper

PORT: int = 8000


@asynccontextmanager
async def lifespan(app: FastAPI):

    async with db_helper.engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)
        await conn.run_sync(Base.metadata.create_all)

    yield


app = FastAPI(lifespan=lifespan)
app.include_router(router=router)


@app.get("/api/hello/")
def hello_index():
    return {"message": "Hello World!"}


if __name__ == "__main__":

    uvicorn.run(
        host="127.0.0.1",
        port=PORT,
        app="main:app",
        reload=True,
    )
