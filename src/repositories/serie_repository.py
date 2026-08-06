from sqlalchemy.orm import Session
from src.dtos.series.series_create import SerieCreateDTO
from src.dtos.series.series_update import SerieUpdateDTO
from src.models.series import Serie
from datetime import datetime, timezone

class SerieRepository:
    
    @staticmethod
    def get_series(db: Session):
        return db.query(Serie).filter(Serie.activo == 1).all()
    
    @staticmethod
    def find_serie(id_serie: int, db: Session):
        return db.query(Serie).filter(
            Serie.id_serie == id_serie,
            Serie.activo == 1
        ).first()
    
    @staticmethod
    def find_serie_including_inactive(id_serie: int, db: Session):
        return db.query(Serie).filter(Serie.id_serie == id_serie).first()
    
    @staticmethod
    def create_serie(dto: SerieCreateDTO, db: Session):
        data = Serie(
            titulo=dto.titulo,
            año_inicio=dto.año_inicio,
            año_fin=dto.año_fin,
            genero=dto.genero,
            temporadas=dto.temporadas,
            episodios=dto.episodios,
            sinopsis=dto.sinopsis,
            estado=dto.estado,
            serie_created_at=datetime.now(timezone.utc),
            serie_updated_at=datetime.now(timezone.utc),
            activo=1
        )
        db.add(data)
        db.flush()
        return data
    
    @staticmethod
    def update_serie(id_serie: int, dto: SerieUpdateDTO, db: Session):
        serie = SerieRepository.find_serie(id_serie, db)
        if not serie:
            return None
        
        if dto.titulo is not None:
            serie.titulo = dto.titulo
        if dto.año_inicio is not None:
            serie.año_inicio = dto.año_inicio
        if dto.año_fin is not None:
            serie.año_fin = dto.año_fin
        if dto.genero is not None:
            serie.genero = dto.genero
        if dto.temporadas is not None:
            serie.temporadas = dto.temporadas
        if dto.episodios is not None:
            serie.episodios = dto.episodios
        if dto.sinopsis is not None:
            serie.sinopsis = dto.sinopsis
        if dto.estado is not None:
            serie.estado = dto.estado
        
        serie.serie_updated_at = datetime.now(timezone.utc)
        db.flush()
        return serie
    
    @staticmethod
    def delete_serie(id_serie: int, db: Session):
        serie = SerieRepository.find_serie(id_serie, db)
        if not serie:
            return None
        
        serie.activo = 0
        serie.serie_updated_at = datetime.now(timezone.utc)
        db.flush()
        return serie
    
    @staticmethod
    def restore_serie(id_serie: int, db: Session):
        serie = SerieRepository.find_serie_including_inactive(id_serie, db)
        if not serie or serie.activo == 1:
            return None
        
        serie.activo = 1
        serie.serie_updated_at = datetime.now(timezone.utc)
        db.flush()
        return serie