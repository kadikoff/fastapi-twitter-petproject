import logging

from fastapi import FastAPI, HTTPException, Request, status
from fastapi.exceptions import RequestValidationError
from fastapi.responses import ORJSONResponse

log = logging.getLogger(__name__)


def register_errors_handlers(app: FastAPI):
    """Регистрирует в приложении FastAPI обработчики исключений"""

    @app.exception_handler(HTTPException)
    async def custom_error_handler_http(
        request: Request, exc: HTTPException
    ) -> ORJSONResponse:
        log.error("Error: %s", exc.detail)
        return ORJSONResponse(
            status_code=exc.status_code,
            content={
                "result": False,
                "error_type": exc.status_code,
                "error_message": exc.detail,
            },
        )

    @app.exception_handler(RequestValidationError)
    async def custom_error_handler_validation(
        request: Request, exc: RequestValidationError
    ) -> ORJSONResponse:
        log.error("Error: %s", exc.errors())
        return ORJSONResponse(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            content={
                "result": False,
                "error_type": status.HTTP_422_UNPROCESSABLE_ENTITY,
                "error_message": exc.errors(),
            },
        )

    @app.exception_handler(Exception)
    async def custom_error_handler_sqlalchemy(
        request: Request, exc: Exception
    ) -> ORJSONResponse:
        log.error("Error: %s", str(exc))
        return ORJSONResponse(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            content={
                "result": False,
                "error_type": status.HTTP_500_INTERNAL_SERVER_ERROR,
                "error_message": f"Server error: {str(exc)}",
            },
        )
