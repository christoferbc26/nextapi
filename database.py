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
    # Intentar obtener la URL completa de la variable de entorno
    database_url = os.getenv("DATABASE_URL")
    if database_url:
        # SOLUCIÓN IPv6: Cambiar a usar Connection Pooling de Supabase
        # Reemplazar conexión directa con pooling para evitar problemas IPv6
        if "db.mnpyqqnmkimfbbnmgyal.supabase.co:5432" in database_url:
            # Cambiar a connection pooling (puerto 6543 en lugar de 5432)
            pooling_url = database_url.replace(
                "db.mnpyqqnmkimfbbnmgyal.supabase.co:5432",
                "aws-0-us-east-1.pooler.supabase.com:6543"
            )
            # Añadir parámetros específicos para pooling
            if "?" not in pooling_url:
                pooling_params = [
                    "sslmode=require",
                    "connect_timeout=30"
                ]
                pooling_url += "?" + "&".join(pooling_params)
            
            print(f"ℹ️ Usando Supabase Connection Pooling para resolver IPv6")
            return pooling_url
        
        # Si no es la URL problemática, usar tal como está
        return database_url
    
    # Si no existe DATABASE_URL, construir usando variables individuales
    # Usar connection pooling por defecto
    db_host = os.getenv("DB_HOST", "aws-0-us-east-1.pooler.supabase.com")
    db_port = os.getenv("DB_PORT", "6543")  # Puerto de pooling
    db_name = os.getenv("DB_NAME", "postgres")
    db_user = os.getenv("DB_USER", "postgres")
    db_password = os.getenv("DB_PASSWORD", "christofer26")
    
    # Codificar la contraseña para URL
    encoded_password = quote_plus(db_password)
    
    # Parámetros para pooling
    params = [
        "sslmode=require",
        "connect_timeout=30"
    ]
    
    base_url = f"postgresql://{db_user}:{encoded_password}@{db_host}:{db_port}/{db_name}"
    return f"{base_url}?{'&'.join(params)}"

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
    try:
        engine = create_engine(
            SQLALCHEMY_DATABASE_URL,
            poolclass=pool.NullPool,  # NullPool es ideal para pgbouncer
            connect_args=connect_args,
            echo=False,  # Cambiar a True para debug si es necesario
        )
        
        # Probar la conexión
        with engine.connect() as conn:
            conn.execute(text("SELECT 1"))
        
        print("✅ Engine creado exitosamente con Connection Pooling")
        return engine
        
    except Exception as e:
        print(f"❌ Error creando engine con pooling: {e}")
        raise e

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
