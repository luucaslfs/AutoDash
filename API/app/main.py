from fastapi import FastAPI, HTTPException, Depends
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.ext.asyncio import AsyncSession
from .api.v1.dashboard import dashboard_router
import httpx
import os
from dotenv import load_dotenv
from .models import UserCreate, UserUpdate, UserInDB, GitHubCallbackRequest
from .database import get_db
from .services import crud
from .core.config import settings

# Load environment variables
load_dotenv()

app = FastAPI()

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],  # Replace with your frontend URL
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(dashboard_router, prefix="/api/v1")

# GitHub App credentials
GITHUB_CLIENT_ID = settings.GH_CLIENT_ID
GITHUB_CLIENT_SECRET = settings.GH_CLIENT_SECRET
GITHUB_CALLBACK_URL = "http://localhost:3000/github/callback"  # Update this to your frontend callback URL

@app.post("/github/callback")
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
            "user": UserInDB.from_orm(db_user).dict()
        }
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@app.get("/users/{user_id}", response_model=UserInDB)
async def read_user(user_id: int, db: AsyncSession = Depends(get_db)):
    db_user = await crud.get_user(db, user_id=user_id)
    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return db_user

@app.put("/users/{user_id}", response_model=UserInDB)
async def update_user(user_id: int, user: UserUpdate, db: AsyncSession = Depends(get_db)):
    db_user = await crud.get_user(db, user_id=user_id)
    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return await crud.update_user(db, db_user=db_user, user_update=user)

@app.delete("/users/{user_id}", response_model=UserInDB)
async def delete_user(user_id: int, db: AsyncSession = Depends(get_db)):
    db_user = await crud.get_user(db, user_id=user_id)
    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return await crud.delete_user(db, user_id=user_id)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)