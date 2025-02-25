from pydantic_settings import BaseSettings, SettingsConfigDict
import os

class Settings(BaseSettings):
    APP_NAME: str = "AutoDash API"
    DEBUG_MODE: bool = True
    DATABASE_URL: str = "sqlite:///./autodash.db"
    TEST_DATABASE_URL: str = "sqlite:///./test.db"
    POSTGRES_USER: str
    POSTGRES_PASSWORD: str
    POSTGRES_DB: str
    OPENAI_API_KEY: str	
    CLAUDE_API_KEY: str
    GH_CALLBACK_URL: str
    GH_CLIENT_ID: str
    GH_CLIENT_SECRET: str
    GH_APP_NAME: str
    GH_APP_ID: int

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding='utf-8'
    )

    @property
    def DATABASE_URL_TO_USE(self):
        return self.TEST_DATABASE_URL if os.getenv("TESTING") else self.DATABASE_URL
    
settings = Settings()