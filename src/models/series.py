from sqlalchemy import Column, Integer, String, DateTime
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
    
    episodios = Column(
        Integer,
        nullable=True
    )
    
    serie_created_at = Column(
        DateTime,
        nullable=False,
        default=datetime.now(timezone.utc)
    )
    sinopsis = Column(
        String(32),
        nullable=True
    )
    
    estado = Column(
        String(20),
        nullable=True
    )
    
    serie_updated_at = Column(
        DateTime,
        nullable=False,
        default=datetime.now(timezone.utc),
        onupdate=datetime.now(timezone.utc)
    )
    
    activo = Column(
        Integer,
        nullable=False,
        default=1,
        comment="Indica si la relación está activa (1) o inactiva (0)"
    )
    
    # Relación con ColeccionSerie
    coleccion_series = relationship(
        "ColeccionSerie",
        back_populates="serie",
        cascade="all, delete-orphan"
    )