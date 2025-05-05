from fastapi import FastAPI, HTTPException, Request, status
from fastapi.responses import JSONResponse
from pydantic import ValidationError


def register_errors_handlers(app: FastAPI):

    @app.exception_handler(HTTPException)
    async def custom_error_handler_http(
        request: Request, exc: HTTPException
    ) -> JSONResponse:
        return JSONResponse(
            status_code=exc.status_code,
            content={
                "result": False,
                "error_type": exc.status_code,
                "error_message": exc.detail,
            },
        )

    @app.exception_handler(ValidationError)
    async def custom_error_handler_validation(
        request: Request, exc: ValidationError
    ) -> JSONResponse:
        return JSONResponse(
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
    ) -> JSONResponse:
        return JSONResponse(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            content={
                "result": False,
                "error_type": status.HTTP_500_INTERNAL_SERVER_ERROR,
                "error_message": f"Server error: {str(exc)}",
            },
        )
