import base64

from fastapi import FastAPI, Depends, HTTPException, status
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, Engine
import services  # Tutaj trzymamy logikę z poprzedniej rozmowy (Ollama, Connection Factory)
import models
import schemas
from schemas import ConnectionConfig
from config import Settings
from typing import List
from client import Client

settings = Settings()
app = FastAPI()

# Dependency do wewnętrznej bazy
def get_engine():
    engine = create_engine(f"postgresql://{settings.db_user}:{settings.db_pass}@{settings.db_host}/{settings.db_name}")
    # Tworzymy tabelę projektów przy starcie
    models.Base.metadata.create_all(bind=engine)
    try:
        yield engine
    finally:
        engine.dispose()

def get_client():
    client = Client(url=settings.ollama_url, model=settings.ollama_model, login=settings.ollama_user, password=settings.ollama_pass)
    try:
        yield client
    finally:
        client = None


# ---------------------------------------------------------
# AUTORYZACJA (Rejestracja, Logowanie, Zmiana Hasła)
# ---------------------------------------------------------

@app.post("/auth/register", status_code=status.HTTP_201_CREATED)
def register(user_data: schemas.RegisterRequest, eng: Engine = Depends(get_engine)):
    with Session(eng) as session:
        # 1. Sprawdź czy użytkownik lub email już istnieje
        existing_user = session.query(models.User).filter(
            (models.User.email == user_data.email) | 
            (models.User.username == user_data.username)
        ).first()
        
        if existing_user:
            raise HTTPException(
                status_code=400, 
                detail="Użytkownik o takim loginie lub emailu już istnieje."
            )

        # 2. Utwórz użytkownika
        new_user = models.User(
            username=user_data.username,
            email=user_data.email,
            password=user_data.password # Pamiętaj: w produkcji tu powinno być haszowanie!
        )
        
        session.add(new_user)
        session.commit()
        return {"message": "Rejestracja udana"}

@app.post("/auth/login", response_model=schemas.UserResponse)
def login(creds: schemas.LoginRequest, eng: Engine = Depends(get_engine)):
    with Session(eng) as session:
        # Szukamy po username (bo tak loguje się Twój LoginView)
        user = session.query(models.User).filter(models.User.username == creds.username).first()

        if not user or user.password != creds.password:
            raise HTTPException(
                status_code=401, 
                detail="Błędny login lub hasło"
            )

        return user

@app.post("/auth/change-password")
def change_password(data: schemas.ChangePasswordRequest, eng: Engine = Depends(get_engine)):
    with Session(eng) as session:
        user = session.query(models.User).filter(models.User.id == data.user_id).first()

        if not user:
            raise HTTPException(status_code=404, detail="Użytkownik nie znaleziony")

        if user.password != data.old_password:
            raise HTTPException(status_code=400, detail="Stare hasło jest nieprawidłowe")

        user.password = data.new_password
        session.commit()
        
        return {"message": "Hasło zostało zmienione"}
    
# ---------------------------------------------------------
# 1. Obsługa ProjectsView.vue (Lista projektów)
# ---------------------------------------------------------

@app.get("/projects", response_model=List[schemas.ProjectResponse])
def get_projects(eng: Engine = Depends(get_engine)):
    # Mapujemy nazwy kolumn z DB na nazwy pól z Vue (db_host -> dbHost)
    with Session(eng) as session:
        projects = session.query(models.Project).all()
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
def test_connection(config: ConnectionConfig):
    """Sprawdza czy dane wpisane w kreatorze działają."""
    try:
        new_engine = services.create_temp_engine(config)
        with new_engine.connect() as conn:
            pass # Udało się połączyć
        return {"status": "success", "message": "Połączono pomyślnie!"}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@app.post("/projects", status_code=201)
def create_project(project: schemas.ProjectCreate, eng: Engine = Depends(get_engine)):
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
    with Session(eng) as session:
        session.add(db_project)
        session.commit()
    return

# ---------------------------------------------------------
# 3. Obsługa ProjectView.vue (Schema Sidebar & Chat)
# ---------------------------------------------------------

@app.get("/projects/{project_id}/schema")
def get_project_schema_tree(project_id: int, eng: Engine = Depends(get_engine)):
    """
    Zwraca schemat w formacie JSON wymaganym przez PrimeVue Tree.
    """
    with Session(eng) as session:
        project = session.query(models.Project).filter(models.Project.id == project_id).first()
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
    return {"schema": tree_nodes, "database_type": project.db_type}

@app.post("/projects/{project_id}/ask")
def ask_assistant(project_id: int, request: schemas.AskRequest, eng: Engine = Depends(get_engine), client = Depends(get_client)):
    with Session(eng) as session:
        project = session.query(models.Project).filter(models.Project.id == project_id).first()
        if not project:
            raise HTTPException(404, "Project not found")
        
    engine = services.get_engine_from_project(project)
    
    # 1. Pobierz schemat tekstowy dla Ollamy
    schema_text = services.get_db_schema(engine)
    
    # 2. Wygeneruj SQL
    generated_sql = services.generate_sql_with_ollama(
        client,
        request.question, 
        schema_text, 
        project.db_type
    )
    
    # Tworzymy wpis w historii
    new_history = models.SQLHistory(
         project_id=project_id,
         question=request.question,
         generated_sql=generated_sql
    )

    session.add(new_history)
    session.commit()

    return {
        "sql": generated_sql
    }
        
       


@app.post("/projects/{project_id}/run")
def run_sql(project_id: int, request: schemas.RunSQLRequest, eng: Engine = Depends(get_engine)):
    with Session(eng) as session:
        project = session.query(models.Project).filter(models.Project.id == project_id).first()
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


#do testow, sam w sobie jest zbedny
@app.post("/projects/{project_id}/history")
def save_history(project_id: int, history: schemas.HistoryCreate, eng: Engine = Depends(get_engine)):
    with Session(eng) as session:
        # Sprawdzamy czy projekt istnieje
        project = session.query(models.Project).filter(models.Project.id == project_id).first()
        if not project:
            raise HTTPException(404, "Project not found")

        # Tworzymy wpis w historii
        new_entry = models.SQLHistory(
            project_id=project_id,
            question=history.question,
            generated_sql=history.generated_sql
        )
        
        session.add(new_entry)
        session.commit()
        
        return {"status": "saved", "id": new_entry.id}


@app.get("/projects/{project_id}/history", response_model=List[schemas.HistoryResponse])
def get_project_history(project_id: int, eng: Engine = Depends(get_engine)):
    with Session(eng) as session:

        project = session.query(models.Project).filter(models.Project.id == project_id).first()
        if not project:
            raise HTTPException(404, "Project not found")

        history = session.query(models.SQLHistory)\
            .filter(models.SQLHistory.project_id == project_id)\
            .order_by(models.SQLHistory.created_at.asc())\
            .all()
            
        return history