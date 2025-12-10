from pydantic_settings import BaseSettings, SettingsConfigDict

# Settingsy są czytane ze zmiennych środowiskowych i są case insensitive (nie ma znaczenia czy zmienne są z dużej czy z małej).
# W pierwszej kolejnośc używane są zmienne środowiskowe (export, docker itp), w drugiej kolejności .env
class Settings(BaseSettings):
    db_user: str
    db_pass: str
    db_host: str
    db_name: str
    ollama_url: str # http://myuser:mypassword@localhost:11434
    ollama_model: str
    ollama_user: str
    ollama_pass: str
    model_config = SettingsConfigDict(
        env_file=".env",
        env_ignore_empty=True,
        extra="ignore"
    )