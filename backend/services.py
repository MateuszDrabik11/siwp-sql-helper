from sqlalchemy import create_engine, text, inspect
# Import flagi do obsługi wielu zapytań w MySQL
from pymysql.constants import CLIENT 

from schemas import ConnectionConfig
from client import Client
from config import Settings

def create_temp_engine(config: ConnectionConfig):
    """Tworzy silnik SQLAlchemy na podstawie konfiguracji z formularza (test połączenia)."""
    url = ""
    connect_args = {} 

    if config.type == "postgres" or config.type == "postgresql":
        url = f"postgresql://{config.username}:{config.password}@{config.host}:{config.port}/{config.database}"
    elif config.type == "mysql":
        url = f"mysql+pymysql://{config.username}:{config.password}@{config.host}:{config.port}/{config.database}"
        # Włącz obsługę wielu zapytań dla MySQL (multi-statements)
        connect_args["client_flag"] = CLIENT.MULTI_STATEMENTS 

    # pool_pre_ping sprawdza czy połączenie żyje przed jego użyciem
    return create_engine(url, pool_pre_ping=True, connect_args=connect_args)

def get_db_schema(engine) -> str:
    """Pobiera strukturę tabel z bazy danych jako tekst (dla AI)."""
    inspector = inspect(engine)
    schema_info = []
    
    for table_name in inspector.get_table_names():
        columns = inspector.get_columns(table_name)
        # Formatujemy jako: nazwa_kolumny (typ)
        cols_desc = ", ".join([f"{col['name']} ({col['type']})" for col in columns])
        schema_info.append(f"Tabela {table_name}: [{cols_desc}]")
        
    if not schema_info:
        return "Baza jest pusta (brak tabel)."
        
    return "\n".join(schema_info)

def generate_sql_with_ollama(client: Client, question: str, schema: str, db_type: str, history: list | None = None) -> str:
    """Wysyła prompt do Ollamy i zwraca czysty SQL."""
    
    # ZAKTUALIZOWANY PROMPT:
    # Dodano punkt 6, który zabrania tworzenia nowych baz danych.
    system_prompt = f"""
    Jesteś ekspertem SQL (dialekt: {db_type}).
    Twoim zadaniem jest zamiana pytania użytkownika na poprawne zapytanie SQL.
    
    Oto aktualny schemat bazy danych:
    {schema}
    
    Zasady:
    1. Zwróć TYLKO kod SQL.
    2. Nie używaj znaczników markdown (```sql).
    3. Nie dodawaj wyjaśnień.
    4. Jeśli pytanie dotyczy modyfikacji danych (INSERT, UPDATE, DELETE, CREATE TABLE), wygeneruj odpowiednie zapytanie.
    5. Używaj tylko tabel i kolumn podanych w schemacie (chyba że użytkownik prosi o utworzenie nowych).
    6. NIE generuj zapytań 'CREATE DATABASE' ani 'USE'. Zakładaj, że jesteś już połączony do właściwej bazy danych. Twórz tabele bezpośrednio.
    """
    
    messages = [{"role": "system", "content": system_prompt}]

    if history:
        for msg in history:
            role = msg.role if hasattr(msg, 'role') else msg['role']
            content = msg.content if hasattr(msg, 'content') else msg['content']
            messages.append({"role": role, "content": content})

    messages.append({"role": "user", "content": question})
    response = client.chat(messages=messages)
    
    sql = response['message']['content']
    # Oczyszczanie wyniku
    sql = sql.replace("```sql", "").replace("```", "").strip()
    return sql

def execute_query(engine, sql: str):
    """
    Wykonuje surowe zapytanie SQL.
    Obsługuje zarówno SELECT, jak i INSERT/UPDATE/DELETE oraz zapytania wielokrotne.
    """
    with engine.connect() as conn:
        result = conn.execute(text(sql))
        conn.commit()

        # Sprawdzamy, czy zapytanie zwraca wiersze (SELECT)
        if result.returns_rows:
            keys = result.keys()
            return [dict(zip(keys, row)) for row in result.fetchall()]
        else:
            # Dla zapytań bez wyników (CREATE, INSERT itp.) zwracamy status
            return [{
                "status": "Sukces", 
                "message": "Operacja wykonana pomyślnie.", 
                "rows_affected": result.rowcount
            }]

def inspect_schema_structure(engine) -> dict:
    """Zwraca słownik {tabela: [kolumny]} do budowania drzewa w frontendzie."""
    inspector = inspect(engine)
    structure = {}
    
    for table_name in inspector.get_table_names():
        columns = inspector.get_columns(table_name)
        cols_desc = [f"{col['name']} ({col['type']})" for col in columns]
        structure[table_name] = cols_desc
        
    return structure

def get_engine_from_project(project_model):
    from sqlalchemy import create_engine
    
    url = ""
    connect_args = {}

    if project_model.db_type == "postgres" or project_model.db_type == "postgresql":
        url = f"postgresql://{project_model.user}:{project_model.password}@{project_model.host}:{project_model.port}/{project_model.db_name}"
    elif project_model.db_type == "mysql":
        url = f"mysql+pymysql://{project_model.user}:{project_model.password}@{project_model.host}:{project_model.port}/{project_model.db_name}"
        # Włącz obsługę wielu zapytań dla MySQL
        connect_args["client_flag"] = CLIENT.MULTI_STATEMENTS
        
    return create_engine(url, connect_args=connect_args)