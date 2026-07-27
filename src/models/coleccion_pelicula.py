from sqlalchemy import Column, Integer, String, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from src.config.database import Base
from datetime import datetime, timezone

class ColeccionPelicula(Base):
    __tablename__ = "coleccionpelicula"
    
    id_coleccion_pelicula = Column(
        Integer,
        primary_key=True,
        index=True,
        autoincrement=True,
        comment="ID único de la relación colección-película"
    )
    
    pelicula_id = Column(
        Integer,
        ForeignKey("pelicula.id_pelicula", ondelete="CASCADE"),
        nullable=False,
        comment="ID de la película (referencia al catálogo)"
    )
    
    id_coleccion = Column(
        Integer,
        ForeignKey("coleccion.id_coleccion", ondelete="CASCADE"),
        nullable=False,
        comment="ID de la colección a la que pertenece"
    )
    
    # Campos específicos de la relación
    fecha_agregado = Column(
        DateTime,
        nullable=False,
        default=datetime.now(timezone.utc),
        comment="Fecha en que se agregó la película a la colección"
    )
    
    opinion = Column(
        String(255),
        nullable=True,
        comment="Opinión personal del usuario sobre la película"
    )
    
    calificacion = Column(
        Integer,
        nullable=True,
        comment="Calificación del usuario (1-5 estrellas)"
    )
    
    nombre_personalizado = Column(
        String(32),
        nullable=True,
        comment="Nombre personalizado que el usuario asigna a la película en su colección"
    )
    
    coleccion_pelicula_created_at = Column(
        DateTime,
        nullable=False,
        default=datetime.now(timezone.utc),
        comment="Fecha de creación del registro"
    )
    
    coleccion_pelicula_update_at = Column(
        DateTime,
        nullable=False,
        default=datetime.now(timezone.utc),
        onupdate=datetime.now(timezone.utc),
        comment="Fecha de última actualización del registro"
    )
    
    # Relaciones
    pelicula = relationship("Pelicula", back_populates="coleccion_peliculas")
    coleccion = relationship("Coleccion", back_populates="coleccion_peliculas")