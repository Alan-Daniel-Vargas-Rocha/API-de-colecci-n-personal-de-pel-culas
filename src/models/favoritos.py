"""
Modelo de la tabla favorito.

Permite a los usuarios marcar películas y series como favoritas.
Un favorito puede ser de tipo 'pelicula' o 'serie'.
"""
from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, UniqueConstraint
from sqlalchemy.orm import relationship
from src.config.database import Base
from datetime import datetime, timezone

class Favorito(Base):
    __tablename__ = "favorito"
    
    id_favorito = Column(
        Integer,
        primary_key=True,
        index=True,
        autoincrement=True,
        comment="ID único del favorito"
    )
    
    id_usuario = Column(
        Integer,
        ForeignKey("usuario.id_usuario", ondelete="CASCADE"),
        nullable=False,
        comment="ID del usuario que marcó el favorito"
    )
    
    tipo = Column(
        String(20),
        nullable=False,
        comment="Tipo de favorito: 'pelicula' o 'serie'"
    )
    
    id_item = Column(
        Integer,
        nullable=False,
        comment="ID de la película o serie (según el tipo)"
    )
    
    fecha_agregado = Column(
        DateTime,
        nullable=False,
        default=datetime.now(timezone.utc),
        comment="Fecha en que se agregó a favoritos"
    )
    
    # Relación con usuario
    usuario = relationship("Usuario", back_populates="favoritos")
    
    # Restricción única para evitar duplicados
    __table_args__ = (
        UniqueConstraint('id_usuario', 'tipo', 'id_item', name='uk_favorito_unico'),
    )