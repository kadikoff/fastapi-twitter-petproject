import uvicorn

from server.core.config import settings
from server.create_app import create_app

app = create_app()

if __name__ == "__main__":

    uvicorn.run(
        host=settings.run.host,
        port=settings.run.port,
        app=settings.run.app,
        reload=settings.run.reload,
    )
