from fastapi import HTTPException
from starlette import status
from sqlalchemy.orm import Session
from datetime import datetime, timezone

from src.dtos.coleccion.coleccion_create import ColeccionCreateDTO
from src.dtos.coleccion.coleccion_update import ColeccionUpdateDTO
from src.models.coleccion import Coleccion
from src.repositories.coleccion_repository import ColeccionRepository

class ColeccionService:
    
    @staticmethod
    def get_colecciones(db: Session):
        return ColeccionRepository.get_colecciones(db=db)
    
    @staticmethod
    def find_coleccion(id_coleccion: int, db: Session):
        coleccion = ColeccionRepository.find_coleccion(id_coleccion=id_coleccion, db=db)
        
        if not coleccion:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Colección no encontrada"
            )
        
        return coleccion
    
    @staticmethod
    def create_coleccion(dto: ColeccionCreateDTO, db: Session):
        data = Coleccion()
        data.id_usuario = dto.id_usuario
        data.nombre = dto.nombre
        data.activo = True  # Asegurar que se crea como activa
        db.add(data)
        db.commit()
        db.refresh(data)
        return data
    
    @staticmethod
    def update_coleccion(id_coleccion: int, dto: ColeccionUpdateDTO, db: Session):
        # Verificar que la colección existe
        coleccion = ColeccionService.find_coleccion(id_coleccion, db)
        
        # Obtener solo los campos que vienen en el DTO
        update_data = dto.dict(exclude_unset=True)
        
        # Actualizar la colección
        updated_coleccion = ColeccionRepository.update_coleccion(id_coleccion, update_data, db)
        
        if updated_coleccion is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Colección no encontrada"
            )
        
        return updated_coleccion
    
    @staticmethod
    def delete_coleccion(id_coleccion: int, db: Session):
        # Verificar que la colección existe
        ColeccionService.find_coleccion(id_coleccion, db)
        
        result = ColeccionRepository.delete_coleccion(id_coleccion, db)
        
        if result is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Colección no encontrada"
            )
        
        return {"message": "Colección eliminada exitosamente"}
    
    @staticmethod
    def restore_coleccion(id_coleccion: int, db: Session):
        result = ColeccionRepository.restore_coleccion(id_coleccion, db)
        
        if result is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Colección no encontrada o ya está activa"
            )
        
        return result
    
    # ============ MÉTODOS PARA PELÍCULAS ============
    
    @staticmethod
    def add_pelicula_to_coleccion(id_coleccion: int, pelicula_id: int, db: Session):
        coleccion = ColeccionRepository.add_pelicula_to_coleccion(id_coleccion, pelicula_id, db)
        
        if coleccion is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Colección o película no encontrada"
            )
        
        return coleccion
    
    @staticmethod
    def remove_pelicula_from_coleccion(id_coleccion: int, pelicula_id: int, db: Session):
        coleccion = ColeccionRepository.remove_pelicula_from_coleccion(id_coleccion, pelicula_id, db)
        
        if coleccion is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Colección o película no encontrada"
            )
        
        return coleccion
    
    # ============ MÉTODOS PARA SERIES ============
    
    @staticmethod
    def add_serie_to_coleccion(id_coleccion: int, id_serie: int, db: Session):
        coleccion = ColeccionRepository.add_serie_to_coleccion(id_coleccion, id_serie, db)
        
        if coleccion is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Colección o serie no encontrada"
            )
        
        return coleccion
    
    @staticmethod
    def remove_serie_from_coleccion(id_coleccion: int, id_serie: int, db: Session):
        coleccion = ColeccionRepository.remove_serie_from_coleccion(id_coleccion, id_serie, db)
        
        if coleccion is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Colección o serie no encontrada"
            )
        
        return coleccion