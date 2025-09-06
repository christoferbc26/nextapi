
# Importar configuración unificada de base de datos optimizada para serverless
from database import engine, SessionLocal, Base, get_db, test_connection

# Re-exportar para mantener compatibilidad
__all__ = ['engine', 'SessionLocal', 'Base', 'get_db', 'test_connection']

# Comentarios sobre la nueva configuración:
# - engine: Objeto que gestiona la conexión a la base de datos, optimizado para Vercel
# - SessionLocal: Clase de sesión para interactuar con la base de datos
# - Base: Clase base para los modelos de SQLAlchemy
# - get_db: Función generadora optimizada para serverless
# - test_connection: Función para verificar la conectividad
