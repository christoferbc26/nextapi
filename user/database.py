# Importar configuración unificada de base de datos
from database import engine, SessionLocal, Base, get_db, test_connection

# Re-exportar para mantener compatibilidad
__all__ = ['engine', 'SessionLocal', 'Base', 'get_db', 'test_connection']
