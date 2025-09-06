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
        # Añadir parámetros para resolver problemas de IPv6 si no están presentes
        if "?" not in database_url:
            # Parámetros para optimizar la conexión en Vercel
            params = [
                "sslmode=require",
                "target_session_attrs=read-write",
                "connect_timeout=30",
                "keepalives_idle=600",
                "keepalives_interval=30",
                "keepalives_count=3"
            ]
            database_url += "?" + "&".join(params)
        return database_url
    
    # Si no existe, construir la URL usando variables individuales
    db_host = os.getenv("DB_HOST", "db.mnpyqqnmkimfbbnmgyal.supabase.co")
    db_port = os.getenv("DB_PORT", "5432")
    db_name = os.getenv("DB_NAME", "postgres")
    db_user = os.getenv("DB_USER", "postgres")
    db_password = os.getenv("DB_PASSWORD", "christofer26")  # Fallback para desarrollo
    
    # Codificar la contraseña para URL
    encoded_password = quote_plus(db_password)
    
    # Parámetros optimizados para Vercel
    params = [
        "sslmode=require",
        "target_session_attrs=read-write",
        "connect_timeout=30",
        "keepalives_idle=600",
        "keepalives_interval=30",
        "keepalives_count=3"
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
    # Configuración de conexión optimizada para Vercel
    connect_args = {
        "sslmode": "require",
        "connect_timeout": 30,  # Aumentado para dar más tiempo
        "application_name": "fastapi-vercel",
        "keepalives_idle": 600,
        "keepalives_interval": 30,
        "keepalives_count": 3,
        # Parámetros adicionales para resolver problemas de IPv6
        "target_session_attrs": "read-write"
    }
    
    try:
        # Intentar crear engine con configuración completa
        engine = create_engine(
            SQLALCHEMY_DATABASE_URL,
            poolclass=pool.StaticPool,  # Cambiar a StaticPool para serverless
            pool_size=1,
            max_overflow=0,
            connect_args=connect_args,
            echo=False,
            pool_pre_ping=True,
            pool_recycle=3600,  # 1 hora
            pool_reset_on_return='commit'
        )
        
        # Probar la conexión
        with engine.connect() as conn:
            conn.execute(text("SELECT 1"))
        
        print("✅ Engine creado exitosamente con StaticPool")
        return engine
        
    except Exception as e:
        print(f"⚠️ Fallo con StaticPool, intentando NullPool: {e}")
        
        # Fallback a NullPool si StaticPool falla
        try:
            engine = create_engine(
                SQLALCHEMY_DATABASE_URL,
                poolclass=pool.NullPool,
                connect_args=connect_args,
                echo=False,
                isolation_level="AUTOCOMMIT"
            )
            print("✅ Engine creado exitosamente con NullPool")
            return engine
        except Exception as e2:
            print(f"❌ Error crítico creando engine: {e2}")
            raise e2

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
