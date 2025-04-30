from fastapi import APIRouter

from .routes_users import router as users_router
from .routes_tweets import router as tweets_router
from .routes_medias import router as medias_router

router = APIRouter()
router.include_router(users_router)
router.include_router(tweets_router)
router.include_router(medias_router)
