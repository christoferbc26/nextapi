
from sqlalchemy import create_engine
#Crea la conexión con la base de datos.
from sqlalchemy.ext.declarative import declarative_base
#Permite definir clases (modelos) que representan tablas en la base de datos.
from sqlalchemy.orm import sessionmaker
#Crea sesiones para interactuar con la base de datos.
from urllib.parse import quote_plus
#Codifica la contraseña para que sea segura en la URL de conexión.

password = quote_plus("christofer26")
#password = quote_plus("P@ssw0rd")
#Codifica la contraseña para evitar problemas con caracteres especiales.
#SQLALCHEMY_DATABASE_URL = f"postgresql://admin:{password}@localhost:5432/nextdb"
#Codifica la contraseña para evitar problemas con caracteres especiales.
#SQLALCHEMY_DATABASE_URL = f"postgresql://postgres:{password}@db.edgjrbcwbxkcwkjvnrsm.supabase.co:5432/postgres"
SQLALCHEMY_DATABASE_URL = f"postgresql://postgres:{password}@db.mnpyqqnmkimfbbnmgyal.supabase.co:5432/postgres"


engine = create_engine(
    SQLALCHEMY_DATABASE_URL,
    connect_args={
        "sslmode": "require"
    }
)
#engine es el objeto que gestina la conexión a la base de datos.
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
#es una clase de sesión que permite interactuar con la base de datos.

Base = declarative_base()
#Base es la clase base para los modelos de SQLAlchemy, que define la estructura de las tablas.

# Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
#Función generadora que crea una sesión de base de datos, la entrega (con yield) y luego la cierra.
#Es útil para frameworks como FastAPI, que usan dependencias para manejar la sesión automáticamente 
#en cada petición.