from sqlalchemy.orm import Session
from src.dtos.coleccionserie.coleccion_serie_update import ColeccionSerieUpdateDTO
from src.dtos.coleccionserie.coleccion_serie_update import ColeccionSerieUpdateDTO
from src.models.coleccionserie import ColeccionSerie
from datetime import datetime, timezone
from typing import Optional

class ColeccionSerieRepository:
    
    @staticmethod
    def get_all_colecciones_series(db: Session):
        return db.query(ColeccionSerie).filter(ColeccionSerie.activo == 1).all()
    
    @staticmethod
    def get_series_from_coleccion(id_coleccion: int, db: Session):
        return db.query(ColeccionSerie).filter(
            ColeccionSerie.id_coleccion == id_coleccion,
            ColeccionSerie.activo == 1
        ).all()
    
    @staticmethod
    def find_coleccion_serie(id_coleccion: int, id_serie: int, db: Session):
        return db.query(ColeccionSerie).filter(
            ColeccionSerie.id_coleccion == id_coleccion,
            ColeccionSerie.id_serie == id_serie,
            ColeccionSerie.activo == 1
        ).first()
    
    @staticmethod
    def add_serie_to_coleccion(
        id_coleccion: int,
        id_serie: int,
        opinion: Optional[str],
        calificacion: Optional[int],
        nombre_personalizado: Optional[str],
        db: Session
    ):
        """Crear relación serie-colección"""
        data = ColeccionSerie(
            id_coleccion=id_coleccion,
            id_serie=id_serie,
            fecha_agregado=datetime.now(timezone.utc),
            opinion=opinion,
            calificacion=calificacion,
            nombre_personalizado=nombre_personalizado,
            coleccion_serie_created_at=datetime.now(timezone.utc),
            coleccion_serie_update_at=datetime.now(timezone.utc),
            activo=1
        )
        db.add(data)
        db.flush()
        return data
    
    @staticmethod
    def update_serie_in_coleccion(
        id_coleccion: int,
        id_serie: int,
        dto: ColeccionSerieUpdateDTO,
        db: Session
    ):
        """Actualizar una relación (prepara, no hace commit)"""
        coleccion_serie = ColeccionSerieRepository.find_coleccion_serie(id_coleccion, id_serie, db)
        if not coleccion_serie:
            return None

        if dto.opinion is not None:
            coleccion_serie.opinion = dto.opinion
        if dto.calificacion is not None:
            coleccion_serie.calificacion = dto.calificacion
        if dto.nombre_personalizado is not None:
            coleccion_serie.nombre_personalizado = dto.nombre_personalizado
        
        coleccion_serie.coleccion_serie_update_at = datetime.now(timezone.utc)
        db.flush()
        return coleccion_serie   
    @staticmethod
    def remove_serie_from_coleccion(id_coleccion: int, id_serie: int, db: Session):
        coleccion_serie = ColeccionSerieRepository.find_coleccion_serie(id_coleccion, id_serie, db)
        if not coleccion_serie:
            return None
        coleccion_serie.activo = 0
        coleccion_serie.coleccion_serie_update_at = datetime.now(timezone.utc)
        db.flush()
        return coleccion_serie