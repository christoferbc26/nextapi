#!/usr/bin/env python3
"""
Script para probar la conexión a la base de datos.
Útil para debugging tanto en desarrollo local como en Vercel.
"""

import os
import sys
from database import test_connection, get_database_url

def main():
    """
    Ejecuta pruebas de conectividad a la base de datos.
    """
    print("=== Test de conexión a la base de datos ===")
    print(f"Python version: {sys.version}")
    print(f"PYTHONPATH: {os.getenv('PYTHONPATH', 'Not set')}")
    
    # Mostrar configuración (sin mostrar contraseña completa)
    db_url = get_database_url()
    safe_url = db_url.replace(db_url.split('@')[0].split(':')[-1], "***") if '@' in db_url else "URL not found"
    print(f"Database URL: {safe_url}")
    
    # Variables de entorno importantes
    env_vars = [
        'DATABASE_URL',
        'DB_HOST', 
        'DB_PORT', 
        'DB_NAME', 
        'DB_USER', 
        'DB_PASSWORD'
    ]
    
    print("\n=== Variables de entorno ===")
    for var in env_vars:
        value = os.getenv(var)
        if value:
            if 'PASSWORD' in var:
                print(f"{var}: {'*' * len(value)}")
            else:
                print(f"{var}: {value}")
        else:
            print(f"{var}: Not set")
    
    # Probar conexión
    print("\n=== Probando conexión ===")
    try:
        if test_connection():
            print("✅ Conexión exitosa!")
            return True
        else:
            print("❌ Error en la conexión")
            return False
    except Exception as e:
        print(f"❌ Error inesperado: {e}")
        return False

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
