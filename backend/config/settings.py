from pydantic_settings import BaseSettings, SettingsConfigDict
from pathlib import Path

class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8")
    
    openai_api_key: str = ""
    openai_api_base: str = "https://api.openai.com/v1"
    openai_model: str = "gpt-4o-mini"
    
    fastapi_host: str = "0.0.0.0"
    fastapi_port: int = 8000
    
    streamlit_port: int = 8501
    
    db_path: str = "./data/example_db.sqlite"
    vector_store_path: str = "./data/faiss_index"
    
    knowledge_dir: str = "./knowledge"
    
    chunk_size: int = 500
    chunk_overlap: int = 50
    top_k: int = 3

settings = Settings()

DATA_DIR = Path("./data")
DATA_DIR.mkdir(parents=True, exist_ok=True)
