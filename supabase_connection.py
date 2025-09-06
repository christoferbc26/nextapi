"""
Configuración alternativa de conexión específica para Supabase
Para resolver problemas de IPv6/IPv4 en entornos serverless
"""
import os
import socket
from urllib.parse import quote_plus
from sqlalchemy import create_engine, pool, event
from sqlalchemy.engine import Engine

def force_ipv4_connection():
    """
    Fuerza el uso de IPv4 para resolver problemas de "Cannot assign requested address"
    """
    # Guardar la función original getaddrinfo
    original_getaddrinfo = socket.getaddrinfo
    
    def getaddrinfo_ipv4_only(host, port, family=0, type=0, proto=0, flags=0):
        return original_getaddrinfo(host, port, socket.AF_INET, type, proto, flags)
    
    # Reemplazar temporalmente con versión IPv4 only
    socket.getaddrinfo = getaddrinfo_ipv4_only

def get_supabase_url_with_params():
    """
    Construye la URL de Supabase con todos los parámetros necesarios
    """
    database_url = os.getenv("DATABASE_URL")
    if not database_url:
        return None
    
    # Si la URL ya tiene parámetros, no los duplicamos
    if "?" in database_url:
        return database_url
    
    # Agregar parámetros específicos para Supabase en Vercel
    params = [
        "sslmode=require",
        "target_session_attrs=read-write",
        "connect_timeout=30",
        "application_name=fastapi-vercel"
    ]
    
    return f"{database_url}?{'&'.join(params)}"

def create_supabase_engine():
    """
    Crea un engine específicamente optimizado para Supabase en Vercel
    """
    # Forzar IPv4
    force_ipv4_connection()
    
    database_url = get_supabase_url_with_params()
    if not database_url:
        raise ValueError("DATABASE_URL not found in environment variables")
    
    # Configuración ultra-conservadora para serverless
    engine = create_engine(
        database_url,
        poolclass=pool.StaticPool,  # Alternativa a NullPool
        pool_size=1,
        max_overflow=0,
        pool_pre_ping=True,
        pool_recycle=-1,  # Nunca recicla automáticamente
        connect_args={
            # Parámetros ya en la URL, pero reforzamos aquí
            "connect_timeout": 30,
            "sslmode": "require",
            "target_session_attrs": "read-write",
            "gssencmode": "disable",
            "tcp_user_timeout": 30000,  # 30 segundos en milisegundos
        },
        echo=False,
        isolation_level="AUTOCOMMIT"
    )
    
    # Event listener para debug de conexiones
    @event.listens_for(engine, "connect")
    def receive_connect(dbapi_connection, connection_record):
        print(f"Connected to database: {dbapi_connection.info}")
    
    return engine

# Test de la nueva configuración
if __name__ == "__main__":
    try:
        engine = create_supabase_engine()
        with engine.connect() as conn:
            result = conn.execute("SELECT 1 as test")
            print("✅ Conexión exitosa con configuración alternativa")
            print(f"Resultado: {result.fetchone()}")
    except Exception as e:
        print(f"❌ Error: {e}")
