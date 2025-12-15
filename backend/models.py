from sqlalchemy import Column, Integer, String, Text
from sqlalchemy.orm import  declarative_base

Base = declarative_base()

class Project(Base):
    __tablename__ = "projects"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    description = Column(String, nullable=True)
    
    # Dane do połączenia z bazą klienta
    db_type = Column(String) # postgres, mysql, etc.
    host = Column(String)
    port = Column(Integer)
    user = Column(String)
    # WAŻNE: W prawdziwej aplikacji hasło powinno być szyfrowane (np. Fernet)
    password = Column(String) 
    db_name = Column(String)
    
    status = Column(String, default="active") # active, offline


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, index=True) # Z RegisterView
    email = Column(String, unique=True, index=True)    # Z RegisterView
    password = Column(String)