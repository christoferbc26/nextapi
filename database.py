"""
Configuración unificada de base de datos optimizada para entorno serverless (Vercel)
"""
import os
from sqlalchemy import create_engine, pool, text
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from urllib.parse import quote_plus

# Configuración de variables de entorno con fallbacks para desarrollo local
def get_database_url():
    # Obtener la URL completa de la variable de entorno
    database_url = os.getenv("DATABASE_URL")
    if database_url:
        # Usar exactamente la URL proporcionada (debe ser la de Connection Pooling)
        # Añadir parámetros solo si no están presentes
        if "?" not in database_url:
            # Parámetros básicos para pooling
            params = [
                "sslmode=require",
                "connect_timeout=30"
            ]
            database_url += "?" + "&".join(params)
        
        print(f"ℹ️ Usando DATABASE_URL configurada")
        return database_url
    
    # Fallback si no existe DATABASE_URL (desarrollo local)
    db_host = os.getenv("DB_HOST", "db.mnpyqqnmkimfbbnmgyal.supabase.co")
    db_port = os.getenv("DB_PORT", "5432")
    db_name = os.getenv("DB_NAME", "postgres")
    db_user = os.getenv("DB_USER", "postgres")
    db_password = os.getenv("DB_PASSWORD", "christofer26")
    
    # Codificar la contraseña para URL
    encoded_password = quote_plus(db_password)
    
    base_url = f"postgresql://{db_user}:{encoded_password}@{db_host}:{db_port}/{db_name}"
    return f"{base_url}?sslmode=require&connect_timeout=30"

# Configuración optimizada para serverless
SQLALCHEMY_DATABASE_URL = get_database_url()

# Configuración del engine optimizada para Vercel/serverless
# Solución para el error "Cannot assign requested address" en IPv6
def create_optimized_engine():
    """
    Crea un engine con configuración específica para resolver problemas de IPv6 en Vercel
    """
    # Configuración de conexión optimizada para Connection Pooling de Supabase
    connect_args = {
        "sslmode": "require",
        "connect_timeout": 30,
        "application_name": "fastapi-vercel"
    }
    
    # NullPool es lo mejor para pgbouncer y serverless
    engine = create_engine(
        SQLALCHEMY_DATABASE_URL,
        poolclass=pool.NullPool,  # NullPool es ideal para pgbouncer
        connect_args=connect_args,
        echo=False,  # Cambiar a True para debug si es necesario
    )
    
    print("✅ Engine creado exitosamente (conexión se probará cuando se use)")
    return engine

# Crear el engine usando la función optimizada
engine = create_optimized_engine()

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
