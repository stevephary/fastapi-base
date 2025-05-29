from fastapi import APIRouter
from app.auth.route import router as auth_router
from app.user.route import router as user_router


api_router = APIRouter()

api_router.include_router(
    router = auth_router,
    prefix="/auth",
    tags=["auth"]
)

api_router.include_router(
    router = user_router,
    prefix="/user",
    tags=["user"]
)