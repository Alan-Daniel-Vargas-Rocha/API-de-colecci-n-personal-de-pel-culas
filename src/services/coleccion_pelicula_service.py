from fastapi import HTTPException
from sqlalchemy.exc import IntegrityError
from starlette import status
from sqlalchemy.orm import Session
from src.dtos.coleccion_pelicula.coleccion_pelicula_create import ColeccionPeliculaCreateDTO
from src.dtos.coleccion_pelicula.coleccion_pelicula_update import ColeccionPeliculaUpdateDTO
from src.repositories.coleccion_pelicula_repository import ColeccionPeliculaRepository

class ColeccionPeliculaService:
    @staticmethod
    def get_colecciones_peliculas(db: Session):
        return ColeccionPeliculaRepository.get_all_colecciones_peliculas(db=db)
    
    @staticmethod
    def find_coleccion_pelicula(id_coleccion: int, id_pelicula: int, db: Session):
        coleccion_pelicula = ColeccionPeliculaRepository.find_coleccion_pelicula(id_coleccion, id_pelicula, db)
        if not coleccion_pelicula:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Relación colección-película no encontrada"
            )
        return coleccion_pelicula

    @staticmethod
    def add_pelicula_to_coleccion(
        id_coleccion: int,
        id_pelicula: int,
        dto: ColeccionPeliculaCreateDTO,
        db: Session
    ):
        # Validación preventiva fuera del bloque de escritura
        existe = ColeccionPeliculaRepository.find_coleccion_pelicula(id_coleccion, id_pelicula, db)
        if existe:
            raise HTTPException(400, "Esta película ya está en la colección")
        
        try:
            nuevo = ColeccionPeliculaRepository.add_pelicula_to_coleccion(
                id_coleccion=id_coleccion,
                id_pelicula=id_pelicula,
                opinion=dto.opinion,
                calificacion=dto.calificacion,
                nombre_personalizado=dto.nombre_personalizado,
                db=db
            )
            db.commit()
            db.refresh(nuevo)
            return nuevo
        except IntegrityError:
            db.rollback()
            raise HTTPException(400, "La relación ya existe en el sistema.")
        except Exception as e:
            db.rollback()
            raise HTTPException(500, f"Error interno: {str(e)}")

    @staticmethod
    def update_coleccion_pelicula(
        id_coleccion: int,
        id_pelicula: int,
        dto: ColeccionPeliculaUpdateDTO,
        db: Session
    ):
        # CORRECCIÓN 1: Validación preventiva fuera del try
        ColeccionPeliculaService.find_coleccion_pelicula(id_coleccion, id_pelicula, db)
        
        try:
            updated = ColeccionPeliculaRepository.update_coleccion_pelicula(
                id_coleccion=id_coleccion,
                id_pelicula=id_pelicula,
                dto=dto,
                db=db
            )
            if updated is None:
                raise HTTPException(404, "Relación no encontrada")
            
            db.commit()
            db.refresh(updated)
            return updated
        except Exception as e:
            db.rollback()
            raise HTTPException(400, f"No se pudo actualizar: {str(e)}")

    @staticmethod
    def delete_coleccion_pelicula(id_coleccion: int, id_pelicula: int, db: Session):
        # CORRECCIÓN 2: Validación preventiva fuera del try
        ColeccionPeliculaService.find_coleccion_pelicula(id_coleccion, id_pelicula, db)
        
        try:
            result = ColeccionPeliculaRepository.delete_coleccion_pelicula(
                id_coleccion=id_coleccion,
                id_pelicula=id_pelicula,
                db=db
            )
            if result is None:
                raise HTTPException(404, "Relación no encontrada")
            
            db.commit()
            return {"message": "Película removida de la colección exitosamente"}
        except Exception as e:
            db.rollback()
            raise HTTPException(400, f"No se pudo eliminar: {str(e)}")
