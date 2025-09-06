"""
Configuración unificada de base de datos optimizada para entorno serverless (Vercel)
"""
import os
from sqlalchemy import create_engine, pool
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from urllib.parse import quote_plus

# Configuración de variables de entorno con fallbacks para desarrollo local
def get_database_url():
    # Intentar obtener la URL completa de la variable de entorno
    database_url = os.getenv("DATABASE_URL")
    if database_url:
        return database_url
    
    # Si no existe, construir la URL usando variables individuales
    db_host = os.getenv("DB_HOST", "db.mnpyqqnmkimfbbnmgyal.supabase.co")
    db_port = os.getenv("DB_PORT", "5432")
    db_name = os.getenv("DB_NAME", "postgres")
    db_user = os.getenv("DB_USER", "postgres")
    db_password = os.getenv("DB_PASSWORD", "christofer26")  # Fallback para desarrollo
    
    # Codificar la contraseña para URL
    encoded_password = quote_plus(db_password)
    
    return f"postgresql://{db_user}:{encoded_password}@{db_host}:{db_port}/{db_name}"

# Configuración optimizada para serverless
SQLALCHEMY_DATABASE_URL = get_database_url()

# Configuración del engine optimizada para Vercel/serverless
engine = create_engine(
    SQLALCHEMY_DATABASE_URL,
    poolclass=pool.NullPool,  # Importante para serverless - evita problemas de conexión
    connect_args={
        "sslmode": "require",
        "connect_timeout": 10,  # Timeout de conexión más corto
        "application_name": "fastapi-vercel",  # Identificar la aplicación en logs
    },
    echo=False,  # Cambiar a True solo para debugging
    pool_pre_ping=True,  # Verifica conexiones antes de usarlas
    pool_recycle=300,  # Recicla conexiones cada 5 minutos
)

# SessionLocal con configuración para serverless
SessionLocal = sessionmaker(
    autocommit=False, 
    autoflush=False, 
    bind=engine,
    expire_on_commit=False  # Importante para serverless
)

Base = declarative_base()

# Dependency optimizada para serverless
def get_db():
    """
    Dependency que proporciona sesiones de base de datos.
    Optimizada para entorno serverless.
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# Función para verificar la conexión
def test_connection():
    """
    Función para probar la conexión a la base de datos.
    Útil para debugging.
    """
    try:
        with engine.connect() as connection:
            result = connection.execute("SELECT 1")
            return True
    except Exception as e:
        print(f"Error de conexión: {e}")
        return False
