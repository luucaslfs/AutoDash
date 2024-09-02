from fastapi import APIRouter, HTTPException, Depends
import httpx
from sqlalchemy.ext.asyncio import AsyncSession
from ...models import UserCreate, UserUpdate, UserInDB, GitHubCallbackRequest
from ...database import get_db
from ...services import crud
from ...core.config import settings

# GitHub App credentials
GITHUB_CLIENT_ID = settings.GH_CLIENT_ID
GITHUB_CLIENT_SECRET = settings.GH_CLIENT_SECRET
GITHUB_CALLBACK_URL = "http://localhost:3000/github/callback"  # Update this to frontend callback URL

github_router = APIRouter()

@github_router.post("/github/callback")
async def github_callback(request: GitHubCallbackRequest, db: AsyncSession = Depends(get_db)):
    try:
        # Exchange code for access token
        token_url = "https://github.com/login/oauth/access_token"
        token_params = {
            "client_id": GITHUB_CLIENT_ID,
            "client_secret": GITHUB_CLIENT_SECRET,
            "code": request.code,
            "redirect_uri": GITHUB_CALLBACK_URL,
        }
        headers = {"Accept": "application/json"}

        async with httpx.AsyncClient() as client:
            token_response = await client.post(token_url, params=token_params, headers=headers)

        if token_response.status_code != 200:
            raise HTTPException(status_code=400, detail=f"Failed to obtain access token: {token_response.text}")

        token_data = token_response.json()
        access_token = token_data.get("access_token")

        if not access_token:
            raise HTTPException(status_code=400, detail="Access token not found in response")

        # Fetch user information
        user_url = "https://api.github.com/user"
        user_headers = {
            "Authorization": f"token {access_token}",
            "Accept": "application/json",
        }

        async with httpx.AsyncClient() as client:
            user_response = await client.get(user_url, headers=user_headers)

        if user_response.status_code != 200:
            raise HTTPException(status_code=400, detail=f"Failed to fetch user information: {user_response.text}")

        github_user_data = user_response.json()

        # Create or update user in database
        user_data = UserCreate(
            github_id=github_user_data["id"],
            login=github_user_data["login"],
            name=github_user_data.get("name"),
            email=github_user_data.get("email"),
            avatar_url=github_user_data.get("avatar_url")
        )
        
        db_user = await crud.get_user_by_github_id(db, github_id=user_data.github_id)
        if db_user:
            db_user = await crud.update_user(db, db_user=db_user, user_update=UserUpdate(**user_data.dict()))
        else:
            db_user = await crud.create_user(db, user=user_data)

        # Return access token and user information
        return {
            "access_token": access_token,
            "user": UserInDB.model_dump(db_user).dict()
        }
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))