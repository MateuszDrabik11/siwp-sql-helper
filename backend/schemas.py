from pydantic import BaseModel
from typing import Optional, List, Any, Dict


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
class AskHistory(BaseModel):
    role: str
    content: str

class AskRequest(BaseModel):
    question: str
    history: List[AskHistory] | None = None

class RunSQLRequest(BaseModel):
    sql: str

class QueryResult(BaseModel):
    columns: List[str]
    data: List[dict]
    generated_sql: Optional[str] = None

class ConnectionConfig(BaseModel):
    host: str
    port: int
    type: str
    username: str
    password: str
    database: str

# Dla RegisterView.vue
class RegisterRequest(BaseModel):
    username: str
    email: str
    password: str
    # confirmPassword sprawdzasz na frontendzie, backendu to nie obchodzi

# Dla LoginView.vue
class LoginRequest(BaseModel):
    username: str # W Vue zmienna nazywa się 'login', ale wyślemy ją jako 'username'
    password: str

# Dla NewPasswordView.vue
class ChangePasswordRequest(BaseModel):
    user_id: int      # Frontend musi wiedzieć czyje hasło zmieniać (bo nie mamy tokenów)
    old_password: str # 'currentPassword' w Vue
    new_password: str # 'newPassword' w Vue

# To co odsyłamy do frontendu po zalogowaniu
class UserResponse(BaseModel):
    id: int
    username: str
    email: str

    class Config:
        from_attributes = True