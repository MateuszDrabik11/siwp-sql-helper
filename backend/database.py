from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base

# Nazwa pliku bazy danych, który powstanie w Twoim folderze
SQLALCHEMY_DATABASE_URL = "sqlite:///./app_internal.db"

# Tworzenie silnika (engine). 
# check_same_thread=False jest potrzebne tylko dla SQLite w FastAPI
engine = create_engine(
    SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False}
)

# Fabryka sesji - będziesz jej używać w main.py (SessionLocal)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Klasa bazowa dla Twoich modeli (używana w models.py)
Base = declarative_base()