from sqlalchemy import Column, Integer, String, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from src.config.database import Base
from datetime import datetime, timezone

class Serie(Base):
    __tablename__ = "series"
    
    id_serie = Column(
        Integer,
        primary_key=True,
        index=True,
        autoincrement=True
    )
    
    titulo = Column(
        String(32),
        nullable=False
    )
    
    año_inicio = Column(
        Integer,
        nullable=True
    )
    
    año_fin = Column(
        Integer,
        nullable=True
    )
    
    genero = Column(
        String(30),
        nullable=False
    )
    
    temporadas = Column(
        Integer,
        nullable=True
    )
    
    serie_created_at = Column(
        DateTime,
        nullable=False,
        default=datetime.now(timezone.utc)
    )
    
    serie_updated_at = Column(
        DateTime,
        nullable=False,
        default=datetime.now(timezone.utc),
        onupdate=datetime.now(timezone.utc)
    )
    
    # Relación con ColeccionSerie
    coleccion_series = relationship(
        "ColeccionSerie",
        back_populates="serie",
        cascade="all, delete-orphan"
    )