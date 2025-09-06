#!/usr/bin/env python3
"""
Script para diagnosticar problemas con la tabla customer
"""
import os
import sys
from sqlalchemy import create_engine, text
from urllib.parse import quote_plus

def test_table_connection():
    """Prueba la conexión y verifica la tabla customer"""
    
    # Obtener DATABASE_URL
    database_url = os.getenv("DATABASE_URL")
    if not database_url:
        print("❌ DATABASE_URL no encontrada")
        return False
    
    print(f"✅ DATABASE_URL configurada")
    
    # Crear engine simple para prueba
    try:
        engine = create_engine(database_url)
        
        with engine.connect() as conn:
            print("✅ Conexión exitosa")
            
            # Verificar si la tabla existe en public schema
            result = conn.execute(text("""
                SELECT EXISTS (
                    SELECT FROM information_schema.tables 
                    WHERE table_schema = 'public' 
                    AND table_name = 'customer'
                );
            """))
            exists_public = result.scalar()
            print(f"Tabla 'customer' en schema 'public': {'✅ Existe' if exists_public else '❌ No existe'}")
            
            # Verificar si la tabla existe en sales schema
            result = conn.execute(text("""
                SELECT EXISTS (
                    SELECT FROM information_schema.tables 
                    WHERE table_schema = 'sales' 
                    AND table_name = 'customer'
                );
            """))
            exists_sales = result.scalar()
            print(f"Tabla 'customer' en schema 'sales': {'✅ Existe' if exists_sales else '❌ No existe'}")
            
            # Si existe en algún schema, mostrar la estructura
            if exists_public:
                print("\n=== Estructura de la tabla en schema public ===")
                result = conn.execute(text("""
                    SELECT column_name, data_type, is_nullable, column_default
                    FROM information_schema.columns
                    WHERE table_schema = 'public' AND table_name = 'customer'
                    ORDER BY ordinal_position;
                """))
                for row in result:
                    print(f"  {row.column_name}: {row.data_type} ({'NULL' if row.is_nullable == 'YES' else 'NOT NULL'}) {f'DEFAULT {row.column_default}' if row.column_default else ''}")
            
            if exists_sales:
                print("\n=== Estructura de la tabla en schema sales ===")
                result = conn.execute(text("""
                    SELECT column_name, data_type, is_nullable, column_default
                    FROM information_schema.columns
                    WHERE table_schema = 'sales' AND table_name = 'customer'
                    ORDER BY ordinal_position;
                """))
                for row in result:
                    print(f"  {row.column_name}: {row.data_type} ({'NULL' if row.is_nullable == 'YES' else 'NOT NULL'}) {f'DEFAULT {row.column_default}' if row.column_default else ''}")
            
            # Verificar si el schema sales existe
            result = conn.execute(text("""
                SELECT EXISTS (
                    SELECT FROM information_schema.schemata 
                    WHERE schema_name = 'sales'
                );
            """))
            sales_schema_exists = result.scalar()
            print(f"\nSchema 'sales': {'✅ Existe' if sales_schema_exists else '❌ No existe'}")
            
            return True
            
    except Exception as e:
        print(f"❌ Error: {e}")
        return False

if __name__ == "__main__":
    print("=== Diagnóstico de tabla customer ===")
    success = test_table_connection()
    sys.exit(0 if success else 1)
