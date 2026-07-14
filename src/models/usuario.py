from sqlalchemy import Column, Integer, String, Boolean, DateTime
from sqlalchemy.orm import relationship
from src.config.database import Base
from datetime import datetime

class Usuario(Base):
    __tablename__ = "usuario"
    
    id_usuario = Column(
        Integer,
        primary_key=True,
        index=True,
        autoincrement=True
    )
    
    nombre = Column(
        String(32),
        nullable=False
    )
    
    email = Column(
        String(30),
        nullable=False,
        unique=True
    )
    
    created_at = Column(
        DateTime,
        nullable=True
    )
    
    updated_at = Column(
        DateTime,
        nullable=True
    )
    
    # Relación con colecciones
    colecciones = relationship("Coleccion", back_populates="usuario", cascade="all, delete-orphan")