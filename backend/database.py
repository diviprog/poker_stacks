from sqlalchemy import create_engine # type: ignore
from sqlalchemy.ext.declarative import declarative_base # type: ignore
from sqlalchemy.orm import sessionmaker # type: ignore
import os

BASE_DIR = os.path.dirname(os.path.abspath(__file__))  # Get the absolute path of the backend directory
DATABASE_URL = f"sqlite:///{os.path.join(BASE_DIR, 'games.db')}"  # Ensure it always points to backend/games.db"
engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False} if "sqlite" in DATABASE_URL else {})
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()