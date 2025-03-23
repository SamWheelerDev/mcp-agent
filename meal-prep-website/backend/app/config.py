import os
from dotenv import load_dotenv
from pydantic_settings import BaseSettings

# Load environment variables
load_dotenv()


class Settings(BaseSettings):
    """Application settings."""

    # API settings
    API_V1_STR: str = "/api/v1"
    PROJECT_NAME: str = "Meal Prep Assistant"

    # Database settings
    DATABASE_URL: str = os.getenv("DATABASE_URL", "sqlite:///./meal_prep.db")

    # Anthropic API settings
    ANTHROPIC_API_KEY: str = os.getenv("ANTHROPIC_API_KEY")
    ANTHROPIC_MODEL: str = "claude-3-7-sonnet-latest"

    # CORS settings
    CORS_ORIGINS: list = ["http://localhost:3000", "http://localhost:5173"]

    class Config:
        env_file = ".env"


# Create settings instance
settings = Settings()
