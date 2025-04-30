from fastapi import FastAPI, HTTPException, Request
from fastapi.responses import JSONResponse
from sqlalchemy.exc import SQLAlchemyError


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

    @app.exception_handler(SQLAlchemyError)
    async def custom_error_handler_sqlalchemy(
        request: Request, exc: SQLAlchemyError
    ) -> JSONResponse:
        return JSONResponse(
            status_code=520,
            content={
                "result": False,
                "error_type": 520,
                "error_message": exc.__str__(),
            },
        )
