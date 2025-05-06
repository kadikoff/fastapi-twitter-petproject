from fastapi import FastAPI

from .log_new_request import log_new_requests


def register_middlewares(app: FastAPI):
    """Регистрирует middlewares в приложении FastAPI"""

    app.middleware("http")(log_new_requests)
