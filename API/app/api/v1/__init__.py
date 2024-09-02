from fastapi import APIRouter
from .dashboard import dashboard_router
from .user import user_router
from .github_callback import github_router

router = APIRouter()

router.include_router(dashboard_router, tags=["dashboard"])
router.include_router(user_router, tags=["user"])
router.include_router(github_router, tags=["github login"])