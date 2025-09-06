from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    DATABASE_URL: str = "postgresql://postgres:christofer26@db.mnpyqqnmkimfbbnmgyal.supabase.co:5432/postgres"
    
    class Config:
        env_file = ".env"

settings = Settings()
