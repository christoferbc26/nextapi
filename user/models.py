from sqlalchemy import Column, Integer, String, TIMESTAMP, text
from .database import Base

class User(Base):
    __tablename__ = "user"
    __table_args__ = {"schema": "login"}

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String(50), unique=True, nullable=False, index=True)
    email = Column(String(255), unique=True, nullable=False, index=True)
    password_hash = Column(String(255), nullable=False)
    created_at = Column(TIMESTAMP(timezone=True), nullable=False, server_default=text('NOW()'))
    updated_at = Column(TIMESTAMP(timezone=True))
