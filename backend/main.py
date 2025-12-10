# from fastapi import FastAPI

# app = FastAPI()


# @app.get("/")
# async def root():
#     return {"message": "Hello World"}


# @app.get("/hello/{name}")
# async def say_hello(name: str):
#     return {"message": f"Hello {name}"}

#===========================

# from fastapi import FastAPI, HTTPException
# from schemas import QueryRequest, QueryResponse
# from services import get_engine, get_db_schema, generate_sql_with_ollama, execute_query

# app = FastAPI(title="Asystent SQL")

# @app.post("/ask", response_model=QueryResponse)
# def ask_database(request: QueryRequest):
#     engine = None
#     try:
#         # 1. Połącz z bazą danych wskazaną przez użytkownika
#         engine = get_engine(request.db_config)
        
#         # 2. Pobierz schemat (kontekst dla AI)
#         schema_context = get_db_schema(engine)
        
#         # 3. Wygeneruj SQL przez Ollamę
#         sql_query = generate_sql_with_ollama(
#             question=request.question,
#             schema=schema_context,
#             db_type=request.db_config.type
#         )
        
#         # 4. Wykonaj zapytanie
#         results = execute_query(engine, sql_query)
        
#         return QueryResponse(
#             question=request.question,
#             generated_sql=sql_query,
#             result=results
#         )

#     except Exception as e:
#         # Łapiemy błędy połączenia, błędy SQL lub błędy Ollamy
#         raise HTTPException(status_code=400, detail=str(e))
    
#     finally:
#         # WAŻNE: Zamykamy silnik po każdym żądaniu, żeby nie zapchać bazy połączeniami
#         if engine:
#             engine.dispose()

# if __name__ == "__main__":
#     import uvicorn
#     uvicorn.run(app, host="0.0.0.0", port=8000)


from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
from sqlalchemy import create_engine
import services  # Tutaj trzymamy logikę z poprzedniej rozmowy (Ollama, Connection Factory)
import models
import schemas
from database import SessionLocal, engine as internal_engine # Konfiguracja Twojej bazy SQLite
from typing import List

# Tworzymy tabelę projektów przy starcie
models.Base.metadata.create_all(bind=internal_engine)

app = FastAPI()

# Dependency do wewnętrznej bazy
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# ---------------------------------------------------------
# 1. Obsługa ProjectsView.vue (Lista projektów)
# ---------------------------------------------------------

@app.get("/projects", response_model=List[schemas.ProjectResponse])
def get_projects(db: Session = Depends(get_db)):
    # Mapujemy nazwy kolumn z DB na nazwy pól z Vue (db_host -> dbHost)
    projects = db.query(models.Project).all()
    # Pydantic zrobi mapowanie jeśli skonfigurujemy aliasy, ale ręcznie jest czytelniej:
    return [
        {
            "id": p.id,
            "name": p.name,
            "description": p.description,
            "dbType": p.db_type,
            "dbHost": p.host,
            "dbPort": p.port,
            "dbName": p.db_name,
            "dbUser": p.user,
            "dbPassword": p.password, # W produkcji nigdy nie zwracaj hasła!
            "status": p.status
        } for p in projects
    ]

# ---------------------------------------------------------
# 2. Obsługa NewProjectView.vue (Tworzenie)
# ---------------------------------------------------------

@app.post("/projects/test-connection")
def test_connection(config: schemas.ProjectCreate):
    """Sprawdza czy dane wpisane w kreatorze działają."""
    try:
        # Używamy serwisu z poprzedniej rozmowy
        engine = services.create_temp_engine(config)
        with engine.connect() as conn:
            pass # Udało się połączyć
        return {"status": "success", "message": "Połączono pomyślnie!"}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@app.post("/projects", response_model=schemas.ProjectResponse)
def create_project(project: schemas.ProjectCreate, db: Session = Depends(get_db)):
    db_project = models.Project(
        name=project.name,
        description=project.description,
        db_type=project.dbType,
        host=project.dbHost,
        port=project.dbPort,
        db_name=project.dbName,
        user=project.dbUser,
        password=project.dbPassword, # Pamiętaj o szyfrowaniu!
        status="active"
    )
    db.add(db_project)
    db.commit()
    db.refresh(db_project)
    
    # Mapowanie zwrotne
    project_dict = project.dict()
    project_dict['id'] = db_project.id
    project_dict['status'] = db_project.status
    return project_dict

# ---------------------------------------------------------
# 3. Obsługa ProjectView.vue (Schema Sidebar & Chat)
# ---------------------------------------------------------

@app.get("/projects/{project_id}/schema")
def get_project_schema_tree(project_id: int, db: Session = Depends(get_db)):
    """
    Zwraca schemat w formacie JSON wymaganym przez PrimeVue Tree.
    """
    project = db.query(models.Project).filter(models.Project.id == project_id).first()
    if not project:
        raise HTTPException(status_code=404, detail="Project not found")

    engine = services.get_engine_from_project(project)
    
    # Używamy services do pobrania surowych metadanych
    raw_metadata = services.inspect_schema_structure(engine) 
    
    # Transformacja do formatu PrimeVue Tree
    # key, label, icon, children
    tree_nodes = []
    
    # Zakładamy schemat 'public' dla uproszczenia, można to rozbudować
    public_node = {
        "key": "0",
        "label": "public",
        "icon": "pi pi-database",
        "children": []
    }
    
    for idx, (table_name, columns) in enumerate(raw_metadata.items()):
        table_key = f"0-{idx}"
        table_node = {
            "key": table_key,
            "label": table_name,
            "icon": "pi pi-table",
            "children": []
        }
        
        for col_idx, col_def in enumerate(columns):
            # col_def to np. "id (INTEGER)"
            col_node = {
                "key": f"{table_key}-{col_idx}",
                "label": col_def,
                "icon": "pi pi-tag",
                "selectable": False
            }
            table_node["children"].append(col_node)
            
        public_node["children"].append(table_node)
        
    tree_nodes.append(public_node)
    return tree_nodes

@app.post("/projects/{project_id}/ask")
def ask_assistant(project_id: int, request: schemas.AskRequest, db: Session = Depends(get_db)):
    project = db.query(models.Project).filter(models.Project.id == project_id).first()
    if not project:
        raise HTTPException(404, "Project not found")
        
    engine = services.get_engine_from_project(project)
    
    # 1. Pobierz schemat tekstowy dla Ollamy
    schema_text = services.get_schema_string(engine)
    
    # 2. Wygeneruj SQL
    generated_sql = services.generate_sql_with_ollama(
        request.question, 
        schema_text, 
        project.db_type
    )
    
    return {
        "response": "Here is the SQL query based on your request.",
        "sql": generated_sql
    }

@app.post("/projects/{project_id}/run")
def run_sql(project_id: int, request: schemas.RunSQLRequest, db: Session = Depends(get_db)):
    project = db.query(models.Project).filter(models.Project.id == project_id).first()
    engine = services.get_engine_from_project(project)
    
    try:
        results = services.execute_query(engine, request.sql)
        # Pobieramy klucze z pierwszego rzędu, jeśli są
        columns = list(results[0].keys()) if results else []
        return {
            "columns": columns,
            "data": results
        }
    except Exception as e:
        raise HTTPException(400, detail=f"SQL Error: {str(e)}")