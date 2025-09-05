from sqlalchemy import Column, Integer, String, Text, TIMESTAMP, text
from .database import Base

class Customer(Base):
    __tablename__ = "customer"
    __table_args__ = {"schema": "sales"}

    customer_id = Column(Integer, primary_key=True, index=True)
    first_name = Column(String(100), nullable=False)
    last_name = Column(String(100), nullable=False)
    phone = Column(String(20))
    address = Column(Text)
    created_at = Column(TIMESTAMP, nullable=False, server_default=text('NOW()'))
    update = Column(TIMESTAMP)
