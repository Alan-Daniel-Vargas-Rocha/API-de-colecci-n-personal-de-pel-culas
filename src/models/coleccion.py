from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, Boolean
from sqlalchemy.orm import relationship
from src.config.database import Base
from datetime import datetime, timezone

class Coleccion(Base):
    __tablename__ = "coleccion"
    
    id_coleccion = Column(
        Integer,
        primary_key=True,
        index=True,
        autoincrement=True
    )
    
    id_usuario = Column(
        Integer,
        ForeignKey("usuario.id_usuario", ondelete="CASCADE"),
        nullable=False
    )
    
    nombre = Column(
        String(32),
        nullable=False
    )
    
    coleccion_created_at = Column(
        DateTime,
        nullable=False,
        default=datetime.now(timezone.utc)
    )
    
    coleccion_update_at = Column(
        DateTime,
        nullable=False,
        default=datetime.now(timezone.utc),
        onupdate=datetime.now(timezone.utc)
    )
    activo = Column(
        Boolean,
        nullable=False,
        default=True,
        server_default='1' 
    )
    
    # Relación con Usuario
    usuario = relationship("Usuario", back_populates="colecciones")
    
    # Relación con ColeccionPelicula (existente)
    coleccion_peliculas = relationship(
        "ColeccionPelicula", 
        back_populates="coleccion",
        cascade="all, delete-orphan"
    )
    
    # Relación con ColeccionSerie 
    coleccion_series = relationship(
        "ColeccionSerie", 
        back_populates="coleccion",
        cascade="all, delete-orphan"
    )