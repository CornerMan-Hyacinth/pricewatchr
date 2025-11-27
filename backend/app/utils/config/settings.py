from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf8",
        case_sensitive=False,
        extra="ignore"
    )
    
    DATABASE_URL: str
    AUTH_SECRET_KEY: str
    EMAIL_FROM: str
    SMTP_SERVER: str
    SMTP_PORT: int
    SMTP_USER: str
    SMTP_PASS: str
    
# Create a singleton instance
settings = Settings()