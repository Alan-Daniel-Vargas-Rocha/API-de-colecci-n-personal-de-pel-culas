from fastapi import HTTPException
from starlette import status

from sqlalchemy.orm import Session
from datetime import datetime, timezone


from src.dtos.coleccion_pelicula.coleccion_pelicula_create import  ColeccionPeliculaCreateDTO
from src.dtos.coleccion_pelicula.coleccion_pelicula_update import  ColeccionPeliculaUpdateDTO
from src.models.coleccion_pelicula import ColeccionPelicula
from src.repositories.coleccion_pelicula_repository import ColeccionPeliculaRepository

class ColeccionPeliculaService:
    
    @staticmethod
    def get_colecciones_peliculas(db: Session): 
        return ColeccionPeliculaRepository.get_colecciones_peliculas(db=db)
    
    @staticmethod
    def find_coleccion_pelicula(coleccion_id: int, pelicula_id: int, db: Session):
        coleccion_pelicula = ColeccionPeliculaRepository.find_coleccion_pelicula(
            coleccion_id = coleccion_id,
            pelicula_id = pelicula_id,
            db = db
        )
        
        if not coleccion_pelicula:
            raise HTTPException(
                status_code = status.HTTP_404_NOT_FOUND,
                detail = "Collection movie not found"
            )
        
        return coleccion_pelicula
    
    @staticmethod
    def create_coleccion_pelicula(dto: ColeccionPeliculaCreateDTO, db: Session):                
        # Create data
        data = ColeccionPelicula(
            id_coleccion = dto.id_coleccion,
            pelicula_id = dto.pelicula_id,
            fecha_agregado = datetime.now(timezone.utc),
            opinion = dto.opinion,
            calificacion = dto.calificacion,
            nombre_personalizado = dto.nombre_personalizado
        )
        
        # Return result
        return ColeccionPeliculaRepository.create_coleccion_pelicula(data = data, db = db)
    
    @staticmethod
    def update_coleccion_pelicula(
        coleccion_id: int,
        pelicula_id: int,
        dto: ColeccionPeliculaUpdateDTO,
        db: Session
    ):
    # 1. Buscar la relación
        coleccion_pelicula = ColeccionPeliculaService.find_coleccion_pelicula(
            coleccion_id=coleccion_id,
            pelicula_id=pelicula_id,
            db=db
        )
    
    # 2. Actualizar campos
        if dto.opinion is not None:
            coleccion_pelicula.opinion = dto.opinion
        if dto.calificacion is not None:
            coleccion_pelicula.calificacion = dto.calificacion
        if dto.nombre_personalizado is not None:  
            coleccion_pelicula.nombre_personalizado = dto.nombre_personalizado
    
    # 3. Actualizar timestamp
        coleccion_pelicula.coleccion_pelicula_update_at = datetime.now(timezone.utc)
    
    # 4. Guardar
        db.commit()
        db.refresh(coleccion_pelicula)
    
        return coleccion_pelicula

    @staticmethod
    def delete_coleccion_pelicula(coleccion_id: int, pelicula_id: int, db: Session):
    # Primero buscar el registro existente
        coleccion_pelicula = ColeccionPeliculaService.find_coleccion_pelicula(
            coleccion_id=coleccion_id,
            pelicula_id=pelicula_id,
            db=db
        )
    
    # Eliminar el registro
        db.delete(coleccion_pelicula)
        db.commit()
    
        return True