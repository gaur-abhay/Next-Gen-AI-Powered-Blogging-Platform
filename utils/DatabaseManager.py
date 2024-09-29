# DatabaseManager.py
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base

DATABASE_URL = "sqlite:///./sqlite-arise-dev"

Base = declarative_base()

class DatabaseManager:
    """Database Manager Class"""

    def __init__(self):
        self._engine = create_engine(DATABASE_URL)

        self._SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=self._engine)

    def init_db(self):
        """Initialize the database"""
        Base.metadata.create_all(self._engine)

    def get_db(self):
        """Return a SQLAlchemy session"""
        db = self._SessionLocal()
        try:
            yield db
        finally:
            db.close()
