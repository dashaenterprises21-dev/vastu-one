"""
Vastu One - Database Setup
SQLAlchemy + SQLite (development) / PostgreSQL (production)
"""

from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent
DB_PATH = BASE_DIR / "vastu_one.db"

# SQLite for development
DATABASE_URL = f"sqlite:///{DB_PATH}"

# For production, switch to:
# DATABASE_URL = "postgresql://user:password@localhost/vastu_one"

engine = create_engine(
    DATABASE_URL,
    connect_args={"check_same_thread": False} if "sqlite" in DATABASE_URL else {},
    echo=False,
)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()


def get_db():
    """Dependency for FastAPI routes"""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def init_db():
    """Create all tables"""
    from database import models  # Import to register models
    Base.metadata.create_all(bind=engine)
    print("[INFO] Database initialized")