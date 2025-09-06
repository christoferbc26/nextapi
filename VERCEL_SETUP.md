# Configuración de Vercel para FastAPI con Supabase

## Variables de entorno requeridas en Vercel

Para solucionar el error de conexión, debes configurar las siguientes variables de entorno en el dashboard de Vercel:

### Método 1: URL completa (Recomendado)

```
DATABASE_URL=postgresql://postgres:christofer26@db.mnpyqqnmkimfbbnmgyal.supabase.co:5432/postgres
```

### Método 2: Variables individuales (Alternativo)

```
DB_HOST=db.mnpyqqnmkimfbbnmgyal.supabase.co
DB_PORT=5432
DB_NAME=postgres
DB_USER=postgres
DB_PASSWORD=christofer26
PYTHONPATH=.
```

## Pasos para configurar en Vercel:

1. Ve a tu proyecto en el dashboard de Vercel
2. Clickea en "Settings"
3. Ve a la sección "Environment Variables"
4. Agrega cada variable con su valor correspondiente
5. Asegúrate de seleccionar todos los entornos (Production, Preview, Development)

## Cambios implementados para solucionar el error:

### 1. Configuración de SQLAlchemy optimizada para serverless
- `poolclass=pool.NullPool`: Evita problemas de conexión en funciones serverless
- `connect_timeout=10`: Timeout más corto para evitar timeouts largos
- `pool_pre_ping=True`: Verifica conexiones antes de usarlas
- `expire_on_commit=False`: Importante para serverless

### 2. Configuración de Vercel actualizada
- `maxLambdaSize`: Aumentado para manejar dependencias de PostgreSQL
- `maxDuration`: Configurado para operaciones de base de datos
- Variables de entorno configuradas

### 3. Eliminación de credenciales hardcodeadas
- Todas las contraseñas ahora se obtienen de variables de entorno
- Fallbacks configurados para desarrollo local

## Verificación local

Puedes probar la conexión localmente ejecutando:

```bash
python test_db_connection.py
```

## Problemas comunes y soluciones:

### Error "Cannot assign requested address"
- **Causa**: Configuración de pool de conexiones inadecuada para serverless
- **Solución**: Usar `NullPool` y configuración optimizada ✅ Implementado

### Error de timeout
- **Causa**: Conexiones que tardan mucho en establecerse
- **Solución**: `connect_timeout=10` ✅ Implementado

### Error de SSL
- **Causa**: Supabase requiere SSL
- **Solución**: `sslmode=require` ✅ Implementado

### Variables de entorno no encontradas
- **Causa**: Variables no configuradas en Vercel
- **Solución**: Configurar en Vercel dashboard ⚠️ Pendiente

## Próximos pasos:

1. Configurar las variables de entorno en Vercel
2. Redesplegar la aplicación
3. Verificar los logs en Vercel para confirmar que la conexión funciona
4. Probar los endpoints de la API

## Comandos útiles para deployment:

```bash
# Verificar archivos antes del deployment
ls -la

# Probar conexión local
python test_db_connection.py

# Redesplegar en Vercel (si tienes Vercel CLI)
vercel --prod
```
