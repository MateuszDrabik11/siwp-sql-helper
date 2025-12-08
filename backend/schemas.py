from pydantic import BaseModel
from typing import Optional, List, Any

# --- NewProjectView.vue ---
class ProjectCreate(BaseModel):
    name: str
    description: Optional[str] = None
    dbType: str  # np. 'postgres'
    dbHost: str
    dbPort: int
    dbName: str
    dbUser: str
    dbPassword: str

class ProjectResponse(ProjectCreate):
    id: int
    status: str
    
    class Config:
        from_attributes = True

# --- ProjectView.vue (Czat) ---
class AskRequest(BaseModel):
    question: str

class RunSQLRequest(BaseModel):
    sql: str

class QueryResult(BaseModel):
    columns: List[str]
    data: List[dict]
    generated_sql: Optional[str] = None