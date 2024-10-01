from datetime import datetime
from typing import Optional, List
from enum import Enum
from sqlalchemy import Column, Integer, String, DateTime
from sqlalchemy.ext.declarative import declarative_base
from pydantic import BaseModel

Base = declarative_base()

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    github_id = Column(Integer, unique=True, index=True)
    login = Column(String, unique=True, index=True)
    name = Column(String, nullable=True)
    email = Column(String, nullable=True)
    avatar_url = Column(String, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)

# Pydantic models for API
class UserBase(BaseModel):
    github_id: int
    login: str
    name: Optional[str] = None
    email: Optional[str] = None
    avatar_url: Optional[str] = None

class UserCreate(UserBase):
    pass

class UserUpdate(BaseModel):
    name: Optional[str] = None
    email: Optional[str] = None
    avatar_url: Optional[str] = None

class UserInDB(UserBase):
    id: int
    created_at: datetime

    class Config:
        from_attributes = True

class AIModelEnum(str, Enum):
    CLAUDE = "claude"
    OPENAI = "openai"

class TableData(BaseModel):
    columns: List[str]
    data: List[List]

class GitHubCallbackRequest(BaseModel):
    code: str

class GenerateDashboardRequest(BaseModel):
    table_data: 'TableData'
    model: AIModelEnum = AIModelEnum.CLAUDE # Default set to Claude

class DownloadDashboardRequest(BaseModel):
    unique_id: str

class CreateGitHubRepoRequest(BaseModel):
    access_token: str
    repo_name: str
    description: Optional[str] = ""
    table_data: TableData
    generated_code: str