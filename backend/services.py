from sqlalchemy import create_engine, text, inspect
import ollama
from schemas import DBConfig

def get_engine(config: DBConfig):
    """Tworzy silnik SQLAlchemy na podstawie konfiguracji."""
    url = ""
    if config.type == "postgresql":
        url = f"postgresql://{config.user}:{config.password}@{config.host}:{config.port}/{config.db_name}"
    elif config.type == "mysql":
        url = f"mysql+pymysql://{config.user}:{config.password}@{config.host}:{config.port}/{config.db_name}"
    
    # pool_pre_ping sprawdza czy połączenie żyje przed jego użyciem
    return create_engine(url, pool_pre_ping=True)

def get_db_schema(engine) -> str:
    """Pobiera strukturę tabel z bazy danych."""
    inspector = inspect(engine)
    schema_info = []
    
    for table_name in inspector.get_table_names():
        columns = inspector.get_columns(table_name)
        # Formatujemy jako: nazwa_kolumny (typ)
        cols_desc = ", ".join([f"{col['name']} ({col['type']})" for col in columns])
        schema_info.append(f"Tabela {table_name}: [{cols_desc}]")
        
    return "\n".join(schema_info)

def generate_sql_with_ollama(question: str, schema: str, db_type: str) -> str:
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
    
    response = ollama.chat(model='llama3', messages=[ # Upewnij się, że masz ten model (lub np. mistral)
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