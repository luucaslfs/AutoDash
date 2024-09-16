import requests
import logging
from fastapi import HTTPException
from sqlalchemy.orm import Session
from ..models import UserCreate, UserUpdate, UserInDB
from ..core.config import settings
from . import crud
import logging

logger = logging.getLogger(__name__)

def github_oauth_callback(code: str, db: Session):
    try:
        # Exchange code for access token
        token_url = "https://github.com/login/oauth/access_token"
        token_params = {
            "client_id": settings.GH_CLIENT_ID,
            "client_secret": settings.GH_CLIENT_SECRET,
            "code": code,
            "redirect_uri": settings.GH_CALLBACK_URL,
        }
        headers = {"Accept": "application/json"}

        logger.info(f"Sending token request to GitHub")
        token_response = requests.post(token_url, params=token_params, headers=headers)

        if token_response.status_code != 200:
            logger.error(f"Failed to obtain access token. Status: {token_response.status_code}, Response: {token_response.text}")
            raise HTTPException(status_code=400, detail=f"Failed to obtain access token: {token_response.text}")

        token_data = token_response.json()
        logger.info(f"Received token response")
        access_token = token_data.get("access_token")

        if not access_token:
            logger.error("Access token not found in response")
            raise HTTPException(status_code=400, detail="Access token not found in response")

        # Fetch user information
        user_url = "https://api.github.com/user"
        user_headers = {
            "Authorization": f"token {access_token}",
            "Accept": "application/json",
        }

        user_response = requests.get(user_url, headers=user_headers)

        if user_response.status_code != 200:
            logger.error(f"Failed to fetch user information. Status: {user_response.status_code}, Response: {user_response.text}")
            raise HTTPException(status_code=400, detail=f"Failed to fetch user information: {user_response.text}")

        github_user_data = user_response.json()
        logger.info(f"Received GitHub user data: {github_user_data}")

        # Create or update user in database
        user_data = UserCreate(
            github_id=github_user_data["id"],
            login=github_user_data["login"],
            name=github_user_data.get("name"),
            email=github_user_data.get("email"),
            avatar_url=github_user_data.get("avatar_url")
        )
        
        db_user = crud.get_user_by_github_id(db, github_id=user_data.github_id)
        if db_user:
            db_user = crud.update_user(db, db_user=db_user, user_update=UserUpdate(**user_data.model_dump()))
        else:
            db_user = crud.create_user(db, user=user_data)

        # Convert SQLAlchemy model to Pydantic model
        user_in_db = UserInDB(
            id=db_user.id,
            github_id=db_user.github_id,
            login=db_user.login,
            name=db_user.name,
            email=db_user.email,
            avatar_url=db_user.avatar_url,
            created_at=db_user.created_at
        )

        # Return access token and user information
        return {
            "access_token": access_token,
            "user": user_in_db.model_dump()
        }
    except Exception as e:
        logger.exception("Error in github_oauth_callback")
        raise HTTPException(status_code=400, detail=str(e))