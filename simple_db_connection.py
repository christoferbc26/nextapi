"""
Configuración simple de base de datos usando psycopg2 directamente
Para usar en casos donde SQLAlchemy tiene problemas en Vercel
"""
import os
import psycopg2
from psycopg2 import pool
from contextlib import contextmanager
from urllib.parse import urlparse

class SimpleDBConnection:
    def __init__(self):
        self.connection_pool = None
        self._init_pool()
    
    def _get_connection_params(self):
        """Extrae parámetros de conexión de DATABASE_URL"""
        database_url = os.getenv("DATABASE_URL")
        if not database_url:
            raise ValueError("DATABASE_URL not set")
        
        # Parsear la URL
        parsed = urlparse(database_url)
        
        return {
            'host': parsed.hostname,
            'port': parsed.port or 5432,
            'database': parsed.path[1:],  # Remover el '/' inicial
            'user': parsed.username,
            'password': parsed.password,
            'sslmode': 'require',
            'connect_timeout': 30,
            'application_name': 'fastapi-vercel-simple'
        }
    
    def _init_pool(self):
        """Inicializa el pool de conexiones simple"""
        try:
            params = self._get_connection_params()
            # Para serverless, usar pool mínimo
            self.connection_pool = psycopg2.pool.SimpleConnectionPool(
                minconn=1,
                maxconn=1,  # Solo una conexión para serverless
                **params
            )
            print("✅ Pool de conexiones inicializado")
        except Exception as e:
            print(f"❌ Error inicializando pool: {e}")
            raise
    
    @contextmanager
    def get_connection(self):
        """Context manager para obtener conexiones"""
        if not self.connection_pool:
            self._init_pool()
        
        conn = None
        try:
            conn = self.connection_pool.getconn()
            yield conn
        except Exception as e:
            if conn:
                conn.rollback()
            raise e
        finally:
            if conn:
                self.connection_pool.putconn(conn)
    
    def test_connection(self):
        """Prueba la conexión"""
        try:
            with self.get_connection() as conn:
                with conn.cursor() as cur:
                    cur.execute("SELECT 1 as test")
                    result = cur.fetchone()
                    print(f"✅ Conexión simple exitosa: {result}")
                    return True
        except Exception as e:
            print(f"❌ Error en conexión simple: {e}")
            return False

# Instancia global
db_simple = SimpleDBConnection()

# Funciones de conveniencia
def execute_query(query, params=None):
    """Ejecuta una query simple"""
    with db_simple.get_connection() as conn:
        with conn.cursor() as cur:
            cur.execute(query, params)
            if cur.description:  # Si hay resultados
                return cur.fetchall()
            conn.commit()
            return cur.rowcount

def execute_select(query, params=None):
    """Ejecuta una query SELECT"""
    with db_simple.get_connection() as conn:
        with conn.cursor() as cur:
            cur.execute(query, params)
            return cur.fetchall()

# Test
if __name__ == "__main__":
    print("=== Test de conexión simple ===")
    db_simple.test_connection()
