from pydantic import BaseModel
from typing import Literal, List, Any, Optional

# Konfiguracja połączenia, którą wysyła użytkownik
class DBConfig(BaseModel):
    type: Literal["postgresql", "mysql"]
    host: str
    port: int
    user: str
    password: str
    db_name: str

# To, co przychodzi w zapytaniu POST
class QueryRequest(BaseModel):
    db_config: DBConfig
    question: str

# To, co odsyłamy do frontendu
class QueryResponse(BaseModel):
    question: str
    generated_sql: str
    result: List[dict]
    error: Optional[str] = None