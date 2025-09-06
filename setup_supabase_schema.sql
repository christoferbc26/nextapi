-- Script para configurar el schema y tabla en Supabase
-- Ejecuta este script en el SQL Editor de Supabase

-- 1. Crear schema sales si no existe
CREATE SCHEMA IF NOT EXISTS sales;

-- 2. Crear la tabla customer en el schema sales
DROP TABLE IF EXISTS sales.customer;

CREATE TABLE sales.customer (
    customer_id SERIAL PRIMARY KEY,
    first_name VARCHAR(100) NOT NULL,
    last_name VARCHAR(100) NOT NULL,
    phone VARCHAR(20),
    address TEXT,
    created_at TIMESTAMP NOT NULL DEFAULT NOW(),
    "update" TIMESTAMP  -- Usar comillas porque 'update' es palabra reservada
);

-- 3. Crear algunos datos de prueba (opcional)
INSERT INTO sales.customer (first_name, last_name, phone, address) VALUES
    ('Juan', 'Pérez', '+1234567890', '123 Main St'),
    ('María', 'González', '+0987654321', '456 Oak Ave'),
    ('Carlos', 'Rodríguez', '+1122334455', '789 Pine Rd');

-- 4. Verificar que la tabla se creó correctamente
SELECT * FROM sales.customer;

-- 5. Verificar la estructura de la tabla
SELECT 
    column_name, 
    data_type, 
    is_nullable, 
    column_default
FROM information_schema.columns
WHERE table_schema = 'sales' AND table_name = 'customer'
ORDER BY ordinal_position;
