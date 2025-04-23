from fastapi import APIRouter

from .users_routers import router as users_router

router = APIRouter()
router.include_router(users_router)
