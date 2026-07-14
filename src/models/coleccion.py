from sqlalchemy import Column, Integer, String, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from src.config.database import Base
from datetime import datetime

class Coleccion(Base):
    __tablename__ = "coleccion"
    
    id_coleccion = Column(
        Integer,
        primary_key=True,
        index=True,
        autoincrement=True)
    
    id_usuario = Column(
        Integer,
        ForeignKey("usuario.id_usuario", ondelete="CASCADE"),
        nullable=False)
    
    nombre = Column(
        String(32),
        nullable=False)
    
    coleccion_created_at = Column(
        DateTime,
        nullable=False, default=datetime.utcnow)
    
    coleccion_update_at = Column(
        DateTime,
        nullable=False,
        default=datetime.utcnow,
        onupdate=datetime.utcnow)
    
    # Relación con Usuario
    usuario = relationship("Usuario", back_populates="colecciones")
    
    coleccion_peliculas = relationship(
        "ColeccionPelicula", 
        back_populates="coleccion",
        cascade="all, delete-orphan"
    )