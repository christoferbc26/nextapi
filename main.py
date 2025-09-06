"""
Archivo principal para ejecutar la aplicación FastAPI
"""

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from user.main import router as auth_router

# Crear nueva instancia de FastAPI
app = FastAPI(title="NextAPI", description="API para aplicación Next.js")

# Endpoint de prueba en la raíz
@app.get("/")
def root():
    return {"message": "NextAPI funcionando correctamente", "status": "ok", "version": "1.0"}

@app.get("/test")
def test():
    return {"message": "Endpoint de prueba funcionando", "status": "ok"}

# Configurar CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:3000",
        "http://127.0.0.1:3000",
        "http://localhost:3001",
        "http://127.0.0.1:3001",
        "https://*.vercel.app",  # Para tu aplicación en Vercel
        "https://nextapi-christoferbc26.vercel.app",  # Reemplaza con tu dominio exacto de Vercel
        "*"  # Temporalmente para debugging - REMOVER EN PRODUCCIÓN
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
    expose_headers=["*"],
)

# Incluir routers
app.include_router(auth_router)

# Importar routers para customers y autenticación
from customer.main import router as customers_router

# Incluir routers
app.include_router(customers_router)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000, reload=True)
