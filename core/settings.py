import os
from pydantic_settings import BaseSettings, SettingsConfigDict

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
ENV_PATH = os.path.join(BASE_DIR, ".env")

class Settings(BaseSettings):
    PROJECT_NAME: str="Dna Analyzer"
    DEBUG: bool = True
    DATABASE_URL: str
    REDIS_URL: str = "redis://localhost:6379/0" 
    model_config=SettingsConfigDict(env_file=ENV_PATH, env_file_encoding='utf-8')

settings=Settings()