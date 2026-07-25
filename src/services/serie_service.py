from fastapi import HTTPException
from starlette import status
from sqlalchemy.orm import Session
from datetime import datetime, timezone

from src.dtos.series.series_create import SerieCreateDTO
from src.dtos.series.series_update import SerieUpdateDTO
from src.models.series import Serie
from src.repositories.serie_repository import SerieRepository

class SerieService:
    
    @staticmethod
    def get_series(db: Session):
        return SerieRepository.get_series(db=db)
    
    @staticmethod
    def find_serie(id_serie: int, db: Session):
        serie = SerieRepository.find_serie(id_serie=id_serie, db=db)
        
        if not serie:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Serie no encontrada"
            )
        
        return serie
    
    @staticmethod
    def create_serie(dto: SerieCreateDTO, db: Session):
        data = Serie()
        data.titulo = dto.titulo
        data.año_inicio = dto.año_inicio
        data.año_fin = dto.año_fin
        data.genero = dto.genero
        data.temporadas = dto.temporadas
        # Las fechas se asignan automáticamente
        
        db.add(data)
        db.commit()
        db.refresh(data)
        return data
    
    @staticmethod
    def update_serie(id_serie: int, dto: SerieUpdateDTO, db: Session):
        # Verificar que la serie existe
        serie = SerieService.find_serie(id_serie, db)
        
        # Obtener solo los campos que vienen en el DTO
        update_data = dto.dict(exclude_unset=True)
        
        # Actualizar la serie
        updated_serie = SerieRepository.update_serie(id_serie, update_data, db)
        
        if updated_serie is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Serie no encontrada"
            )
        
        return updated_serie
    
    @staticmethod
    def delete_serie(id_serie: int, db: Session):
        # Verificar que la serie existe
        result = SerieService.find_serie(id_serie, db)
        
        result = SerieRepository.delete_serie(id_serie, db)
        
        if result is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Serie no encontrada"
            )
        
        return {"message": "Serie eliminada exitosamente"}