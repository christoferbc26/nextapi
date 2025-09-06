# 🔧 Solución IPv6: Usar Supabase Connection Pooling

## ❌ Problema
Error: `Cannot assign requested address` en Vercel cuando usa IPv6 de Supabase.

## ✅ Solución
Usar **Connection Pooling** de Supabase en lugar de conexión directa a PostgreSQL.

## 📝 Pasos para solucionarlo:

### 1. Obtener la URL de Connection Pooling desde Supabase

1. Ve a tu proyecto en [Supabase Dashboard](https://app.supabase.com)
2. Ve a **Settings** → **Database**
3. En la sección **Connection Pooling**, copia la **Connection string**
4. La URL debería verse así:
   ```
   postgresql://postgres:[PASSWORD]@aws-0-us-east-1.pooler.supabase.com:6543/postgres
   ```

### 2. Actualizar DATABASE_URL en Vercel

1. Ve a tu proyecto en [Vercel Dashboard](https://vercel.com/dashboard)
2. Ve a **Settings** → **Environment Variables**
3. Edita la variable `DATABASE_URL`
4. Reemplaza la URL actual con la URL de Connection Pooling
5. La nueva URL debe usar:
   - **Host**: `aws-0-us-east-1.pooler.supabase.com`
   - **Puerto**: `6543` (en lugar de `5432`)

### 3. Ejemplo de URLs:

**❌ URL directa (problemática)**:
```
postgresql://postgres:password@db.mnpyqqnmkimfbbnmgyal.supabase.co:5432/postgres
```

**✅ URL con Connection Pooling (solución)**:
```
postgresql://postgres:password@aws-0-us-east-1.pooler.supabase.com:6543/postgres
```

### 4. Redesplegar en Vercel

Después de cambiar la variable de entorno, Vercel redesplegará automáticamente.

## 🔍 Verificación

Una vez actualizada la URL, prueba estos endpoints:

1. **Test de conexión**:
   ```
   https://nextapi-iota.vercel.app/customers/debug
   ```

2. **Lista de customers**:
   ```
   https://nextapi-iota.vercel.app/customers/
   ```

## ⚙️ Por qué funciona esta solución:

- **Connection Pooling** usa un host diferente que no tiene problemas IPv6
- **pgbouncer** maneja mejor las conexiones en entornos serverless
- **Puerto 6543** en lugar de **5432** evita el problema de red
- **NullPool** en SQLAlchemy funciona perfectamente con pgbouncer

## 🚨 Importante:
- Usa exactamente la URL de Connection Pooling de tu proyecto en Supabase
- El host puede ser diferente según tu región de Supabase
- Asegúrate de usar el puerto **6543** para pooling
