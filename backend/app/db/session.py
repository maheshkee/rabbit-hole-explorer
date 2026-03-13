from typing import Generator
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, Session

from app.core.config import settings

# 1. engine creation
engine = create_engine(settings.SQLALCHEMY_DATABASE_URI)

# 2. SessionLocal
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# 3. get_db() dependency function
def get_db() -> Generator[Session, None, None]:
    """
    Dependency function for FastAPI to get a database session.
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
