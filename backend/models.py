from sqlalchemy import Column, Integer, String, Text, ForeignKey, DateTime, ForeignKey
from sqlalchemy.orm import  declarative_base, relationship
from datetime import datetime

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
    owner_id = Column(Integer, ForeignKey("users.id"))
    # Relationship back to User
    owner = relationship("User", back_populates="projects")


class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, index=True) # Z RegisterView
    email = Column(String, unique=True, index=True)    # Z RegisterView
    password = Column(String)
    projects = relationship("Project", back_populates="owner")


class SQLHistory(Base):
    __tablename__ = "sql_history"

    id = Column(Integer, primary_key=True, index=True)
    project_id = Column(Integer, ForeignKey("projects.id"))
    question = Column(String)
    generated_sql = Column(Text)
    created_at = Column(DateTime, default=datetime.utcnow)