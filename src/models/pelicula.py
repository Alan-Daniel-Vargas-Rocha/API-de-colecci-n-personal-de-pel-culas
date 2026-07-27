from sqlalchemy import Column, Integer, String, DateTime
from sqlalchemy.orm import relationship
from src.config.database import Base
from datetime import datetime, timezone

class Pelicula(Base):
    __tablename__ = "pelicula"
    
    id_pelicula = Column(
        Integer,
        primary_key=True,
        index=True,
        autoincrement=True
    )
    
    titulo = Column(
        String(32),
        nullable=False
    )
    
    año = Column(
        Integer,
        nullable=True
    )
    
    genero = Column(
        String(30),
        nullable=False
    )
    
    pelicula_created_at = Column(
        DateTime,
        nullable=False,
        default=datetime.now(timezone.utc)
    )
    
    pelicula_updated_at = Column(
        DateTime,
        nullable=False,
        default=datetime.now(timezone.utc),
        onupdate=datetime.now(timezone.utc)
    )
    
    # Relación con ColeccionPelicula
    coleccion_peliculas = relationship(
        "ColeccionPelicula",
        back_populates="pelicula",
        cascade="all, delete-orphan"
    )