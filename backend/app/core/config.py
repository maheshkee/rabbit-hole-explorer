import os
from dotenv import load_dotenv

# Load .env file
load_dotenv(os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))), ".env"))

class Settings:
    PROJECT_NAME: str = "AI Internet Rabbit Hole Explorer"
    VERSION: str = "0.1.0"
    API_V1_STR: str = "/api/v1"

    DATABASE_URL: str = os.getenv("DATABASE_URL", "postgresql+psycopg2://postgres:postgres@localhost:5432/rabbit_hole")
    
    # Free Tier API Keys
    GEMINI_API_KEY: str = os.getenv("GEMINI_API_KEY", "")
    TAVILY_API_KEY: str = os.getenv("TAVILY_API_KEY", "")

    @property
    def SQLALCHEMY_DATABASE_URI(self) -> str:
        url = self.DATABASE_URL
        if url.startswith("postgres://"):
            return url.replace("postgres://", "postgresql+psycopg2://", 1)
        if url.startswith("postgresql://") and not url.startswith("postgresql+psycopg2://"):
            return url.replace("postgresql://", "postgresql+psycopg2://", 1)
        return url

settings = Settings()
