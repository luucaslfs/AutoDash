import base64
import requests
from typing import Dict, Any
from fastapi import HTTPException
import logging

# Configuração de logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class GitHubService:
    def __init__(self, access_token: str):
        self.access_token = access_token
        self.base_url = "https://api.github.com"
        self.headers = {
            "Authorization": f"Bearer {self.access_token}",
            "Accept": "application/vnd.github.v3+json"
        }
        logger.info("GitHubService initialized")

    def create_repository(self, name: str, description: str = "") -> Dict[str, Any]:
        url = f"{self.base_url}/user/repos"
        data = {
            "name": name,
            "description": description,
            "private": False
        }
        logger.info(f"Creating repository {name} with headers: {self.headers}")
        response = requests.post(url, headers=self.headers, json=data)
        if response.status_code != 201:
            raise HTTPException(status_code=response.status_code, detail=f"Failed to create repository: {response.json()}")
        return response.json()

    def create_commit(self, owner: str, repo: str, branch: str, message: str, files: Dict[str, str]) -> Dict[str, Any]:
        for file_path, content in files.items():
            self._create_or_update_file(owner, repo, file_path, message, content, branch)
        return {"message": "Files committed successfully"}

    def _create_or_update_file(self, owner: str, repo: str, path: str, message: str, content: str, branch: str) -> Dict[str, Any]:
        url = f"{self.base_url}/repos/{owner}/{repo}/contents/{path}"
        data = {
            "message": message,
            "content": base64.b64encode(content.encode()).decode(),
            "branch": branch
        }

        # Check if file already exists
        response = requests.get(url, headers=self.headers)
        if response.status_code == 200:
            # File exists, update it
            data["sha"] = response.json()["sha"]
            response = requests.put(url, headers=self.headers, json=data)
        else:
            # File doesn't exist, create it
            response = requests.put(url, headers=self.headers, json=data)

        if response.status_code not in [200, 201]:
            raise HTTPException(status_code=response.status_code, detail=f"Failed to create/update file {path}: {response.json()}")
        return response.json()