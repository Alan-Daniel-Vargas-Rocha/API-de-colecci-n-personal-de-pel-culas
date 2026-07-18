from sqlalchemy import Column, Integer, String, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from src.config.database import Base
from datetime import datetime

class ColeccionPelicula(Base):
    __tablename__ = "coleccionpelicula"
    
    id_coleccion_pelicula = Column(
        Integer,
        primary_key=True,
        index=True,
        autoincrement=True
    )
    
    pelicula_id = Column(
        Integer,
        ForeignKey("pelicula.id_pelicula", ondelete="CASCADE"),
        nullable=False
    )
    
    id_coleccion = Column(
        Integer,
        ForeignKey("coleccion.id_coleccion", ondelete="CASCADE"),
        nullable=False
    )
    
    fecha_agregado = Column(
        DateTime,
        nullable=False,
        default=datetime.utcnow
    )
    
    opinion = Column(
        String(255),
        nullable=True
    )
    
    coleccion_pelicula_created_at = Column(
        DateTime,
        nullable=False,
        default=datetime.utcnow
    )
    
    coleccion_pelicula_update_at = Column(
        DateTime,
        nullable=False,
        default=datetime.utcnow,
        onupdate=datetime.utcnow
    )
    
    calificacion = Column(
        Integer,
        nullable=True
    )
    
    # Relaciones
    coleccion = relationship("Coleccion", back_populates="coleccion_peliculas")
    pelicula = relationship("Pelicula", back_populates="coleccion_peliculas")