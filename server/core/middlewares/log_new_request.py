import logging
from typing import Awaitable, Callable

from fastapi import Request, Response

log = logging.getLogger(__name__)


async def log_new_requests(
    request: Request, call_next: Callable[[Request], Awaitable[Response]]
) -> Response:
    """Логгирование запросов"""

    log.info("Новый %s запрос к %s", request.method, request.url.path)

    return await call_next(request)
