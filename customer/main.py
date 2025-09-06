from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from sqlalchemy import update, text
from datetime import datetime
from . import models, schemas, database
from .database import get_db
from typing import List

# Las tablas deben existir previamente en Supabase
# No crear tablas automáticamente en serverless para evitar errores de conexión

router = APIRouter(
    prefix="/customers",
    tags=["customers"],
)

@router.get("/test")
def test_endpoint():
    """Endpoint de prueba simple sin base de datos"""
    return {"message": "Customer endpoints funcionando correctamente", "status": "ok"}

@router.get("/debug")
def debug_database(db: Session = Depends(get_db)):
    """Endpoint de debug para probar la conexión a la base de datos"""
    try:
        # Probar consulta simple
        result = db.execute(text("SELECT 1 as test"))
        test_result = result.scalar()
        
        # Verificar si la tabla existe
        table_check = db.execute(text("""
            SELECT EXISTS (
                SELECT FROM information_schema.tables 
                WHERE table_schema = 'sales' 
                AND table_name = 'customer'
            )
        """))
        table_exists = table_check.scalar()
        
        # Verificar si el schema sales existe
        schema_check = db.execute(text("""
            SELECT EXISTS (
                SELECT FROM information_schema.schemata 
                WHERE schema_name = 'sales'
            )
        """))
        schema_exists = schema_check.scalar()
        
        return {
            "message": "Conexión a base de datos exitosa",
            "test_query": test_result,
            "sales_schema_exists": schema_exists,
            "customer_table_exists": table_exists,
            "status": "ok"
        }
        
    except Exception as e:
        return {
            "message": "Error en la conexión a base de datos",
            "error": str(e),
            "status": "error"
        }

# get_db ya está importado en la parte superior

@router.post("/", response_model=schemas.Customer)
#este endpoint respondera a peticiones en la ruta /customers/, luego la respuesta 
#sera convertida al modelo customer para asi los datos devueltos tengan el formato correcto
def create_customer(customer: schemas.CustomerCreate, db: Session = Depends(get_db)):
#
    db_customer = models.Customer(**customer.dict())
    db.add(db_customer)
    db.commit()
    db.refresh(db_customer)
    return db_customer

@router.get("/", response_model=List[schemas.Customer])
def list_customers(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    customers = db.query(models.Customer).offset(skip).limit(limit).all()
    return customers

@router.get("/{customer_id}", response_model=schemas.Customer)
def get_customer(customer_id: int, db: Session = Depends(get_db)):
    customer = db.query(models.Customer).filter(models.Customer.customer_id == customer_id).first()
    if customer is None:
        raise HTTPException(status_code=404, detail="Customer not found")
    return customer

@router.put("/{customer_id}", response_model=schemas.Customer)
def update_customer(customer_id: int, customer: schemas.CustomerUpdate, db: Session = Depends(get_db)):
    db_customer = db.query(models.Customer).filter(models.Customer.customer_id == customer_id).first()
    if db_customer is None:
        raise HTTPException(status_code=404, detail="Customer not found")
    
    update_data = customer.dict(exclude_unset=True)
    if update_data:
        update_data["update"] = datetime.now()
        for key, value in update_data.items():
            setattr(db_customer, key, value)
        
        db.commit()
        db.refresh(db_customer)
    return db_customer

@router.delete("/{customer_id}")
def delete_customer(customer_id: int, db: Session = Depends(get_db)):
    customer = db.query(models.Customer).filter(models.Customer.customer_id == customer_id).first()
    if customer is None:
        raise HTTPException(status_code=404, detail="Customer not found")
    
    db.delete(customer)
    db.commit()
    return {"message": "Customer deleted successfully"}
