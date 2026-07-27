from sqlalchemy import Column, Integer, String, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from src.config.database import Base
from datetime import datetime, timezone

class ColeccionSerie(Base):
    __tablename__ = "coleccionserie"
    
    id_coleccion_serie = Column(
        Integer,
        primary_key=True,
        index=True,
        autoincrement=True
    )
    
    serie_id = Column(
        Integer,
        ForeignKey("series.id_serie", ondelete="CASCADE"),
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
        default=datetime.now(timezone.utc)
    )
    
    opinion = Column(
        String(255),
        nullable=True
    )
    
    calificacion = Column(
        Integer,
        nullable=True
    )
    
    nombre_personalizado = Column(
        String(32),
        nullable=True
    )
    
    coleccion_serie_created_at = Column(
        DateTime,
        nullable=False,
        default=datetime.now(timezone.utc)
    )
    
    coleccion_serie_update_at = Column(
        DateTime,
        nullable=False,
        default=datetime.now(timezone.utc),
        onupdate=datetime.now(timezone.utc)
    )
    
    # Relaciones
    serie = relationship("Serie", back_populates="coleccion_series")
    coleccion = relationship("Coleccion", back_populates="coleccion_series")