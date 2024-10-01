import requests
import logging
import pandas as pd
import io
from fastapi import HTTPException
from sqlalchemy.orm import Session
from ..models import UserCreate, UserUpdate, UserInDB, TableData
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

        logger.info(f"Sending token request to GitHub with params: {token_params}")
        token_response = requests.post(token_url, params=token_params, headers=headers)

        logger.info(f"Token response status: {token_response.status_code}")
        logger.info(f"Token response headers: {token_response.headers}")
        logger.info(f"Token response content: {token_response.text}")

        if token_response.status_code != 200:
            logger.error(f"Failed to obtain access token. Status: {token_response.status_code}, Response: {token_response.text}")
            raise HTTPException(status_code=400, detail=f"Failed to obtain access token: {token_response.text}")

        token_data = token_response.json()
        access_token = token_data.get("access_token")
        scope = token_data.get("scope", "")

        logger.info(f"Received token response. Scope: {scope}")


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
        granted_scopes = user_response.headers.get('X-OAuth-Scopes', '').split(', ')
        logger.info(f"Granted scopes: {granted_scopes}")

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

def generate_dashboard_files(table_data: TableData, generated_code: str):
    try:        
        # Criar DataFrame a partir dos dados da tabela
        df = pd.DataFrame(table_data.data, columns=table_data.columns)
        
        # Criar conteúdo CSV usando um buffer de memória
        csv_buffer = io.StringIO()
        df.to_csv(csv_buffer, index=False)
        csv_content = csv_buffer.getvalue()

        # Create the content of the files
        files = {
            "app.py": generated_code,
            "requirements.txt": """
            streamlit
            pandas
            plotly
            matplotlib
            seaborn
            """.strip(),
            "README.md": f"""
            # AutoDash Generated Dashboard

            Este dashboard foi gerado automaticamente pelo AutoDash.

            ## Como executar

            1. Instale as dependências:
            ```
            pip install -r requirements.txt
            ```

            2. Execute o dashboard:
            ```
            streamlit run app.py
            ```

            3. Abra o navegador no endereço indicado pelo Streamlit.
            """.strip(),
            "data.csv": csv_content
        }
        
        logger.info("Created all necessary files for the dashboard")
        
        return files
    except Exception as e:
        logger.exception("Error in generate_dashboard_files")
        raise