from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    APP_NAME: str = "AutoDash API"
    DEBUG_MODE: bool = True
    DATABASE_URL: str
    SYNC_DATABASE_URL: str
    TEST_DATABASE_URL: str = "sqlite+aiosqlite:///./test.db"
    OPENAI_KEY: str	
    CLAUDE_API_KEY: str
    GH_CLIENT_ID: str
    GH_CLIENT_SECRET: str

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding='utf-8'
    )

    @property
    def DATABASE_URL_TO_USE(self):
        return self.TEST_DATABASE_URL if os.getenv("TESTING") else self.DATABASE_URL
    
settings = Settings()