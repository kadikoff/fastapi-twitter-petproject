from contextlib import asynccontextmanager
from typing import Any, AsyncGenerator

import uvicorn
from fastapi import FastAPI

from server.api.routes import router
from server.core.config import BASE_MEDIAS_DIR
from server.core.models import Users, db_helper
from server.error_handlers import register_errors_handlers

PORT: int = 8000


async def create_mock_data() -> None:
    user_1 = Users(name="Artyom Kadikov", api_key="test")
    user_2 = Users(name="Nikita Ivanov", api_key="dev")

    async with db_helper.session_factory() as session:
        session.add_all([user_1, user_2])
        await session.commit()
        await session.close()


@asynccontextmanager
async def lifespan(app: FastAPI) -> AsyncGenerator[None, Any]:

    BASE_MEDIAS_DIR.mkdir(parents=True, exist_ok=True)

    # await create_mock_data()

    yield

    # await db_helper.engine.dispose()


app = FastAPI(lifespan=lifespan)
app.include_router(router=router)
register_errors_handlers(app=app)


if __name__ == "__main__":

    uvicorn.run(
        host="0.0.0.0",
        port=8000,
        app="main:app",
        reload=True,
    )
