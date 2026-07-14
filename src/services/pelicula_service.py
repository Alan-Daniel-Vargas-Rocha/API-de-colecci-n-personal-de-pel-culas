from fastapi import HTTPException
from starlette import status
from sqlalchemy.orm import Session
from datetime import datetime, timezone

from src.dtos.pelicula.pelicula_created import PeliculaCreateDTO
from src.dtos.pelicula.pelicula_update import PeliculaUpdateDTO
from src.models.pelicula import Pelicula  
from src.repositories.pelicula_repository import PeliculaRepository

class PeliculaService:
    
    @staticmethod
    def get_peliculas(db: Session):
        return PeliculaRepository.get_peliculas(db=db)
    
    @staticmethod
    def find_pelicula(id_pelicula: int, db: Session):
        pelicula = PeliculaRepository.find_pelicula(id_pelicula=id_pelicula, db=db)
        
        if not pelicula:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Movie not found"
            )
        
        return pelicula
    
    @staticmethod
    def create_pelicula(dto: PeliculaCreateDTO, db: Session):
       
        data = Pelicula(
            titulo=dto.titulo,  
            año=dto.año,
            genero=dto.genero,
            # activo=dto.activo
        )
        
        # Return result
        return PeliculaRepository.create_pelicula(data=data, db=db)
    
    @staticmethod
    def update_pelicula(id_pelicula: int, dto: PeliculaUpdateDTO, db: Session):
        # Primero verificamos que la película existe
        pelicula = PeliculaService.find_pelicula(id_pelicula, db)
        
        # Actualizamos solo los campos que vienen en el DTO
        update_data = dto.dict(exclude_unset=True)
        
        # Aplicar las actualizaciones
        for key, value in update_data.items():
            if hasattr(pelicula, key):
                setattr(pelicula, key, value)
        
        # Guardamos los cambios
        db.commit()
        db.refresh(pelicula)
        
        return pelicula