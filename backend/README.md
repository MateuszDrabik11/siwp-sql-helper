Żeby odpalic backend: 
cd siwp-sql-helper/backend

uvicorn main:app --reload

dostaniecie link http://127.0.0.1:8000, a na http://127.0.0.1:8000/docs jest swagger. 
na swaggerze mozna przetestowac end pointy zwiazane z bazami danych, nie dziala/nie sprawdzalem ze wzgledow technicznych tego gadania z ai (brak karty graficznej)

do test connection i run sql jest potrzebne polączenie z rzeczywistą bazą danych, moze byc przez dockera. 
ja korzystałem z czegoś takiego: 


terminal: docker run --name test-postgres -e POSTGRES_PASSWORD=tajnehaslo -p 5432:5432 -d postgres


JSON do SWAGGERA: 
{
  "name": "Test Docker DB",
  "description": "Sprawdzamy polaczenie",
  "dbType": "postgres",
  "dbHost": "localhost",
  "dbPort": 5432,
  "dbName": "postgres",
  "dbUser": "postgres",
  "dbPassword": "tajnehaslo"
}