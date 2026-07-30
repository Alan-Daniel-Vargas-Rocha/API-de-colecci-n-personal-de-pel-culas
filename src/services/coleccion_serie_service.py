from fastapi import HTTPException
from starlette import status
from sqlalchemy.orm import Session
from datetime import datetime, timezone

from src.dtos.coleccionserie.coleccion_serie_create import ColeccionSerieCreateDTO
from src.dtos.coleccionserie.coleccion_serie_update import ColeccionSerieUpdateDTO
from src.models.coleccionserie import ColeccionSerie  
from src.repositories.coleccion_series_repository import ColeccionSerieRepository
from src.services.coleccion_service import ColeccionService 
from src.services.serie_service import SerieService

class ColeccionSerieService:
    
    @staticmethod
    def get_series_from_coleccion(id_coleccion: int, db: Session):
        # Verificar que la colección existe
        ColeccionService.find_coleccion(id_coleccion, db)  
        
        return ColeccionSerieRepository.get_series_from_coleccion(
            id_coleccion=id_coleccion, 
            db=db
        )
    
    @staticmethod
    def find_coleccion_serie(id_coleccion: int, id_serie: int, db: Session):
        # Verificar que la colección y serie existen
        ColeccionService.find_coleccion(id_coleccion, db) 
        SerieService.find_serie(id_serie, db)
        
        coleccion_serie = ColeccionSerieRepository.find_coleccion_serie(
            id_coleccion=id_coleccion, 
            id_serie=id_serie, 
            db=db
        )
        
        if not coleccion_serie:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Relación colección-serie no encontrada"
            )
        
        return coleccion_serie
    
    @staticmethod
    def add_serie_to_coleccion(id_coleccion: int, id_serie: int, dto: ColeccionSerieCreateDTO, db: Session):
        # Verificar que la colección y serie existen
        ColeccionService.find_coleccion(id_coleccion, db)  
        SerieService.find_serie(id_serie, db)
        
        # Obtener solo los campos que vienen en el DTO
        data = dto.dict(exclude_unset=True)
        
        coleccion_serie = ColeccionSerieRepository.add_serie_to_coleccion(
            id_coleccion=id_coleccion,
            id_serie=id_serie,
            data=data,
            db=db
        )
        
        if coleccion_serie is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Colección o serie no encontrada"
            )
        
        return coleccion_serie
    
    @staticmethod
    def update_serie_in_coleccion(id_coleccion: int, id_serie: int, dto: ColeccionSerieUpdateDTO, db: Session):
        # Verificar que la colección y serie existen
        ColeccionService.find_coleccion(id_coleccion, db)  
        SerieService.find_serie(id_serie, db)
        
        # Obtener solo los campos que vienen en el DTO
        update_data = dto.dict(exclude_unset=True)
        
        # Actualizar la relación
        updated_coleccion_serie = ColeccionSerieRepository.update_serie_in_coleccion(
            id_coleccion=id_coleccion,
            id_serie=id_serie,
            data=update_data,
            db=db
        )
        
        if updated_coleccion_serie is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Relación colección-serie no encontrada"
            )
        
        return updated_coleccion_serie
    
    @staticmethod
    def remove_serie_from_coleccion(id_coleccion: int, id_serie: int, db: Session):
        # Verificar que la colección y serie existen
        ColeccionService.find_coleccion(id_coleccion, db)  
        SerieService.find_serie(id_serie, db)
        
        result = ColeccionSerieRepository.remove_serie_from_coleccion(
            id_coleccion=id_coleccion,
            id_serie=id_serie,
            db=db
        )
        
        if result is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Relación colección-serie no encontrada"
            )
        
        return {"message": "Serie removida de la colección exitosamente"}