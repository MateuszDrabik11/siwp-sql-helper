# from fastapi import FastAPI

# app = FastAPI()


# @app.get("/")
# async def root():
#     return {"message": "Hello World"}


# @app.get("/hello/{name}")
# async def say_hello(name: str):
#     return {"message": f"Hello {name}"}


from fastapi import FastAPI, HTTPException
from schemas import QueryRequest, QueryResponse
from services import get_engine, get_db_schema, generate_sql_with_ollama, execute_query

app = FastAPI(title="Asystent SQL")

@app.post("/ask", response_model=QueryResponse)
def ask_database(request: QueryRequest):
    engine = None
    try:
        # 1. Połącz z bazą danych wskazaną przez użytkownika
        engine = get_engine(request.db_config)
        
        # 2. Pobierz schemat (kontekst dla AI)
        schema_context = get_db_schema(engine)
        
        # 3. Wygeneruj SQL przez Ollamę
        sql_query = generate_sql_with_ollama(
            question=request.question,
            schema=schema_context,
            db_type=request.db_config.type
        )
        
        # 4. Wykonaj zapytanie
        results = execute_query(engine, sql_query)
        
        return QueryResponse(
            question=request.question,
            generated_sql=sql_query,
            result=results
        )

    except Exception as e:
        # Łapiemy błędy połączenia, błędy SQL lub błędy Ollamy
        raise HTTPException(status_code=400, detail=str(e))
    
    finally:
        # WAŻNE: Zamykamy silnik po każdym żądaniu, żeby nie zapchać bazy połączeniami
        if engine:
            engine.dispose()

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)