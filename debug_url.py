#!/usr/bin/env python3
"""
Script para mostrar exactamente qué DATABASE_URL se está usando
"""
import os

def show_database_config():
    """Muestra la configuración de base de datos actual"""
    print("=== Configuración de Base de Datos ===")
    
    # Mostrar DATABASE_URL
    database_url = os.getenv("DATABASE_URL")
    if database_url:
        # Ocultar password para seguridad
        safe_url = database_url
        if "@" in safe_url:
            parts = safe_url.split("@")
            user_pass = parts[0].split(":")
            if len(user_pass) >= 3:  # postgresql://user:pass
                safe_url = f"{user_pass[0]}:{user_pass[1]}:***@{parts[1]}"
        print(f"DATABASE_URL: {safe_url}")
    else:
        print("DATABASE_URL: No encontrada")
    
    # Mostrar otras variables relacionadas
    postgres_vars = [
        "POSTGRES_URL",
        "POSTGRES_HOST", 
        "POSTGRES_USER",
        "POSTGRES_PASSWORD",
        "POSTGRES_DATABASE"
    ]
    
    print("\n=== Otras variables de PostgreSQL ===")
    for var in postgres_vars:
        value = os.getenv(var)
        if value:
            if "PASSWORD" in var or "pass" in var.lower():
                print(f"{var}: {'*' * len(value)}")
            elif "@" in str(value) and "://" in str(value):
                # Es una URL, ocultarla parcialmente
                safe_value = str(value)
                if "@" in safe_value:
                    parts = safe_value.split("@")
                    user_pass = parts[0].split(":")
                    if len(user_pass) >= 3:
                        safe_value = f"{user_pass[0]}:{user_pass[1]}:***@{parts[1]}"
                print(f"{var}: {safe_value}")
            else:
                print(f"{var}: {value}")
        else:
            print(f"{var}: No encontrada")

if __name__ == "__main__":
    show_database_config()
