from fastapi import HTTPException
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from src.dtos.pelicula.pelicula_created import PeliculaCreateDTO
from src.dtos.pelicula.pelicula_update import PeliculaUpdateDTO
from src.repositories.pelicula_repository import PeliculaRepository

class PeliculaService:
    
    # LECTURAS (sin transacción)
    
    @staticmethod
    def get_peliculas(db: Session):
        return PeliculaRepository.get_peliculas(db=db)
    
    @staticmethod
    def find_pelicula(id_pelicula: int, db: Session):
        pelicula = PeliculaRepository.find_pelicula(id_pelicula, db)
        if not pelicula:
            raise HTTPException(404, "Película no encontrada")
        return pelicula
    
    # CREATE (con transacción)
    
    @staticmethod
    def create_pelicula(dto: PeliculaCreateDTO, db: Session):
        if not dto.titulo or len(dto.titulo.strip()) == 0:
            raise HTTPException(400, "El título es obligatorio")
        
        if len(dto.titulo) > 32:
            raise HTTPException(400, "El título excede los 32 caracteres")
        
        if not dto.genero or len(dto.genero.strip()) == 0:
            raise HTTPException(400, "El género es obligatorio")
        
        if len(dto.genero) > 30:
            raise HTTPException(400, "El género excede los 30 caracteres")
        
        try:
            nueva = PeliculaRepository.create_pelicula(dto, db)
            db.commit()
            db.refresh(nueva)
            return nueva
        except IntegrityError:
            db.rollback()
            raise HTTPException(400, "Error de integridad: la película ya existe o los datos son inválidos")
        except Exception as e:
            db.rollback()
            raise HTTPException(500, f"Error interno del servidor: {str(e)}")
    
    # UPDATE (con transacción)
    
    @staticmethod
    def update_pelicula(id_pelicula: int, dto: PeliculaUpdateDTO, db: Session):
        # CORRECCIÓN 1: Validación preventiva fuera del bloque try
        PeliculaService.find_pelicula(id_pelicula, db)
        
        try:
            updated = PeliculaRepository.update_pelicula(
                id_pelicula=id_pelicula,
                dto=dto,
                db=db
            )
            if updated is None:
                raise HTTPException(404, "Película no encontrada")
            
            db.commit()
            db.refresh(updated)
            return updated
        except IntegrityError:
            db.rollback()
            raise HTTPException(400, "Error de integridad al actualizar la película")
        except Exception as e:
            db.rollback()
            raise HTTPException(400, f"No se pudo actualizar la película: {str(e)}")
    
    # DELETE (soft delete, con transacción)
    
    @staticmethod
    def delete_pelicula(id_pelicula: int, db: Session):

        PeliculaService.find_pelicula(id_pelicula, db)
        
        try:
            result = PeliculaRepository.delete_pelicula(id_pelicula, db)
            if result is None:
                raise HTTPException(404, "Película no encontrada")
            
            db.commit()
            return {"message": "Película eliminada exitosamente"}
        except Exception as e:
            db.rollback()
            raise HTTPException(400, f"No se pudo eliminar la película: {str(e)}")
    
    # RESTORE (con transacción)
    
    @staticmethod
    def restore_pelicula(id_pelicula: int, db: Session):
       
        # alternativo de búsqueda (como find_including_inactive) aquí antes del try para dar un 404 real.
        try:
            result = PeliculaRepository.restore_pelicula(id_pelicula, db)
            if result is None:
                raise HTTPException(404, "Película no encontrada o ya está activa")    
            db.commit()
            db.refresh(result)
            return result
        except HTTPException:
            # Re-lanzamos el 404 si vino de la validación interna
            raise
        except Exception as e:
            db.rollback()
            raise HTTPException(400, f"No se pudo restaurar la película: {str(e)}")
