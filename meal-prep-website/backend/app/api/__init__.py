from fastapi import APIRouter
from .chat import router as chat_router
from .recipes import router as recipes_router
from .calendar import router as calendar_router
from .users import router as users_router
from .onboarding import router as onboarding_router

# Create main API router
api_router = APIRouter()

# Include all routers
api_router.include_router(users_router, prefix="/users", tags=["users"])
api_router.include_router(recipes_router, prefix="/recipes", tags=["recipes"])
api_router.include_router(calendar_router, prefix="/calendar", tags=["calendar"])
api_router.include_router(chat_router, prefix="/chat", tags=["chat"])
api_router.include_router(onboarding_router, prefix="/onboarding", tags=["onboarding"])
