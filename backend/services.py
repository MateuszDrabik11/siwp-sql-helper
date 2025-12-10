from sqlalchemy import create_engine, text, inspect

from schemas import ConnectionConfig
from client import Client

from config import Settings

def create_temp_engine(config: ConnectionConfig):
    """Tworzy silnik SQLAlchemy na podstawie konfiguracji z formularza (test połączenia)."""
    url = ""
    # Frontend wysyła kod bazy (np. 'postgres'), musimy to obsłużyć
    if config.type == "postgres" or config.type == "postgresql":
        url = f"postgresql://{config.username}:{config.password}@{config.host}:{config.port}/{config.database}"
    elif config.type == "mysql":
        url = f"mysql+pymysql://{config.username}:{config.password}@{config.host}:{config.port}/{config.database}"
    
    # pool_pre_ping sprawdza czy połączenie żyje przed jego użyciem
    return create_engine(url, pool_pre_ping=True)

def get_db_schema(engine) -> str:
    """Pobiera strukturę tabel z bazy danych jako tekst (dla AI)."""
    inspector = inspect(engine)
    schema_info = []
    
    for table_name in inspector.get_table_names():
        columns = inspector.get_columns(table_name)
        # Formatujemy jako: nazwa_kolumny (typ)
        cols_desc = ", ".join([f"{col['name']} ({col['type']})" for col in columns])
        schema_info.append(f"Tabela {table_name}: [{cols_desc}]")
        
    return "\n".join(schema_info)

def generate_sql_with_ollama(client: Client, question: str, schema: str, db_type: str) -> str:
    """Wysyła prompt do Ollamy i zwraca czysty SQL."""
    
    system_prompt = f"""
    Jesteś ekspertem SQL (dialekt: {db_type}).
    Twoim zadaniem jest zamiana pytania użytkownika na poprawne zapytanie SQL (SELECT).
    
    Oto schemat bazy danych:
    {schema}
    
    Zasady:
    1. Zwróć TYLKO kod SQL.
    2. Nie używaj znaczników markdown (```sql).
    3. Nie dodawaj wyjaśnień.
    4. Używaj tylko tabel i kolumn podanych w schemacie.
    """
    settings = Settings()
    # Pamiętaj, żeby mieć uruchomione 'ollama serve' w tle
    response = client.chat(messages=[
        {'role': 'system', 'content': system_prompt},
        {'role': 'user', 'content': question},
    ])
    
    # Oczyszczanie wyniku (modele lubią dodawać ```sql na początku)
    sql = response['message']['content']
    sql = sql.replace("```sql", "").replace("```", "").strip()
    return sql

def execute_query(engine, sql: str):
    """Wykonuje surowe zapytanie SQL i zwraca listę słowników."""
    with engine.connect() as conn:
        result = conn.execute(text(sql))
        keys = result.keys()
        return [dict(zip(keys, row)) for row in result.fetchall()]

def inspect_schema_structure(engine) -> dict:
    """Zwraca słownik {tabela: [kolumny]} do budowania drzewa w frontendzie."""
    inspector = inspect(engine)
    structure = {}
    
    for table_name in inspector.get_table_names():
        columns = inspector.get_columns(table_name)
        # Zapisujemy jako listę stringów np. "id (INTEGER)"
        cols_desc = [f"{col['name']} ({col['type']})" for col in columns]
        structure[table_name] = cols_desc
        
    return structure

# Helper do tworzenia silnika z modelu ORM (baza zapisana w systemie)
# Tutaj używamy nazw z models.py (snake_case), więc jest OK
def get_engine_from_project(project_model):
    from sqlalchemy import create_engine
    
    url = ""
    # Obsługa nazw z modelu bazy danych (models.py)
    if project_model.db_type == "postgres" or project_model.db_type == "postgresql":
        url = f"postgresql://{project_model.user}:{project_model.password}@{project_model.host}:{project_model.port}/{project_model.db_name}"
    elif project_model.db_type == "mysql":
        url = f"mysql+pymysql://{project_model.user}:{project_model.password}@{project_model.host}:{project_model.port}/{project_model.db_name}"
        
    return create_engine(url)