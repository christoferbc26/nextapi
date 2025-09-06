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
        # Para Supabase, agregar parámetros adicionales si no están presentes
        if "supabase.co" in database_url and "?" not in database_url:
            database_url += "?sslmode=require&target_session_attrs=read-write"
        return database_url
    
    # Si no existe, construir la URL usando variables individuales
    db_host = os.getenv("DB_HOST", "db.mnpyqqnmkimfbbnmgyal.supabase.co")
    db_port = os.getenv("DB_PORT", "5432")
    db_name = os.getenv("DB_NAME", "postgres")
    db_user = os.getenv("DB_USER", "postgres")
    db_password = os.getenv("DB_PASSWORD", "christofer26")  # Fallback para desarrollo
    
    # Codificar la contraseña para URL
    encoded_password = quote_plus(db_password)
    
    # URL con parámetros optimizados para Supabase
    return f"postgresql://{db_user}:{encoded_password}@{db_host}:{db_port}/{db_name}?sslmode=require&target_session_attrs=read-write"

# Configuración optimizada para serverless
SQLALCHEMY_DATABASE_URL = get_database_url()

# Importar configuración alternativa para casos problemáticos
try:
    from supabase_connection import create_supabase_engine, force_ipv4_connection
    ALTERNATIVE_CONFIG_AVAILABLE = True
except ImportError:
    ALTERNATIVE_CONFIG_AVAILABLE = False

# Configuración del engine optimizada para Vercel/serverless
# Intentar forzar IPv4 si está disponible
if ALTERNATIVE_CONFIG_AVAILABLE:
    try:
        force_ipv4_connection()
    except:
        pass  # Continuar sin IPv4 forzado si falla

# Crear engine con configuración optimizada
try:
    # Intentar con configuración alternativa primero si está disponible
    if ALTERNATIVE_CONFIG_AVAILABLE and os.getenv("VERCEL"):
        engine = create_supabase_engine()
    else:
        # Configuración estándar mejorada
        engine = create_engine(
            SQLALCHEMY_DATABASE_URL,
            poolclass=pool.NullPool,  # Importante para serverless
            connect_args={
                "sslmode": "require",
                "connect_timeout": 30,
                "application_name": "fastapi-vercel",
                "target_session_attrs": "read-write",
                "gssencmode": "disable",
                "options": "-c default_transaction_isolation=read committed"
            },
            echo=False,
            pool_pre_ping=True,
            pool_recycle=300,
            execution_options={"isolation_level": "AUTOCOMMIT"}
        )
except Exception as e:
    print(f"Warning: Failed to create optimized engine: {e}")
    # Fallback a configuración básica
    engine = create_engine(
        SQLALCHEMY_DATABASE_URL,
        poolclass=pool.NullPool,
        connect_args={"sslmode": "require"},
        echo=False
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
