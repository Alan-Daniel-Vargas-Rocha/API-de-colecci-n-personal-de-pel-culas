from fastapi import HTTPException
from sqlalchemy.exc import IntegrityError
from starlette import status
from sqlalchemy.orm import Session
from datetime import datetime, timezone

from src.dtos.pelicula.pelicula_created import PeliculaCreateDTO
from src.dtos.pelicula.pelicula_update import PeliculaUpdateDTO
from src.repositories.pelicula_repository import PeliculaRepository

class PeliculaService:
    
    # ============================================
    # 1️⃣ LECTURAS (sin transacción)
    # ============================================
    
    @staticmethod
    def get_peliculas(db: Session):
        return PeliculaRepository.get_peliculas(db=db)
    
    @staticmethod
    def find_pelicula(id_pelicula: int, db: Session):
        pelicula = PeliculaRepository.find_pelicula(id_pelicula, db)
        
        if not pelicula:
            raise HTTPException(404, "Película no encontrada")
        
        return pelicula
    
    # ============================================
    # 2️⃣ CREATE (con transacción)
    # ============================================
    
    @staticmethod
    def create_pelicula(dto: PeliculaCreateDTO, db: Session):
        # 1. Validaciones de negocio (pre-transacción)
        if not dto.titulo or len(dto.titulo.strip()) == 0:
            raise HTTPException(400, "El título es obligatorio")
        
        if len(dto.titulo) > 32:
            raise HTTPException(400, "El título excede los 32 caracteres")
        
        if not dto.genero or len(dto.genero.strip()) == 0:
            raise HTTPException(400, "El género es obligatorio")
        
        if len(dto.genero) > 30:
            raise HTTPException(400, "El género excede los 30 caracteres")
        
        # 2. Control de transacción
        try:
            # ✅ Delegar al repositorio
            nueva = PeliculaRepository.create_pelicula(dto, db)
            
            # ✅ Confirmar transacción
            db.commit()
            db.refresh(nueva)
            return nueva
            
        except IntegrityError:
            db.rollback()
            raise HTTPException(400, "Error de integridad: la película ya existe o los datos son inválidos")
        except HTTPException:
            raise
        except Exception as e:
            db.rollback()
            raise HTTPException(500, f"Error interno del servidor: {str(e)}")
    
    # ============================================
    # 3️⃣ UPDATE (con transacción)
    # ============================================
    
    @staticmethod
    def update_pelicula(id_pelicula: int, dto: PeliculaUpdateDTO, db: Session):
        try:
            # ✅ Verificar que existe
            PeliculaService.find_pelicula(id_pelicula, db)
            
            # ✅ Delegar al repositorio
            updated = PeliculaRepository.update_pelicula(
                id_pelicula=id_pelicula,
                dto=dto,
                db=db
            )
            
            if updated is None:
                raise HTTPException(404, "Película no encontrada")
            
            # ✅ Confirmar transacción
            db.commit()
            db.refresh(updated)
            return updated
            
        except HTTPException:
            raise
        except IntegrityError:
            db.rollback()
            raise HTTPException(400, "Error de integridad al actualizar la película")
        except Exception as e:
            db.rollback()
            raise HTTPException(400, f"No se pudo actualizar la película: {str(e)}")
    
    # ============================================
    # 4️⃣ DELETE (soft delete, con transacción)
    # ============================================
    
    @staticmethod
    def delete_pelicula(id_pelicula: int, db: Session):
        try:
            # ✅ Verificar que existe
            PeliculaService.find_pelicula(id_pelicula, db)
            
            # ✅ Delegar al repositorio
            result = PeliculaRepository.delete_pelicula(id_pelicula, db)
            
            if result is None:
                raise HTTPException(404, "Película no encontrada")
            
            # ✅ Confirmar transacción
            db.commit()
            return {"message": "Película eliminada exitosamente"}
            
        except HTTPException:
            raise
        except Exception as e:
            db.rollback()
            raise HTTPException(400, f"No se pudo eliminar la película: {str(e)}")
    
    # ============================================
    # 5️⃣ RESTORE (con transacción)
    # ============================================
    
    @staticmethod
    def restore_pelicula(id_pelicula: int, db: Session):
        try:
            result = PeliculaRepository.restore_pelicula(id_pelicula, db)
            if result is None:
                raise HTTPException(404, "Película no encontrada o ya está activa")    
            db.commit()
            db.refresh(result)
            return result
        except Exception as e:
            db.rollback()
            raise HTTPException(400, f"No se pudo restaurar la película: {str(e)}")