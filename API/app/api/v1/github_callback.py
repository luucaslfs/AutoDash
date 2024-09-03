from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from ...models import GitHubCallbackRequest
from ...database import get_db
from ...services.github import github_oauth_callback
import logging

logger = logging.getLogger(__name__)

github_router = APIRouter()

@github_router.post("/github/callback")
async def github_callback(request: GitHubCallbackRequest, db: AsyncSession = Depends(get_db)):
    try:
        return await github_oauth_callback(request.code, db)
    except HTTPException as he:
        logger.error(f"HTTP Exception in github_callback: {he.detail}")
        raise
    except Exception as e:
        logger.exception("Unexpected error in github_callback")
        raise HTTPException(status_code=500, detail="Internal server error")