from fastapi import HTTPException
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session
from src.dtos.coleccion.coleccion_create import ColeccionCreateDTO
from src.dtos.coleccion.coleccion_update import ColeccionUpdateDTO
from src.repositories.coleccion_repository import ColeccionRepository

class ColeccionService:
 
    #  LECTURAS (sin transacción)
    
    @staticmethod
    def get_colecciones(db: Session):
        return ColeccionRepository.get_colecciones(db=db)
    
    @staticmethod
    def find_coleccion(id_coleccion: int, db: Session):
        coleccion = ColeccionRepository.find_coleccion(id_coleccion, db)
        if not coleccion:
            raise HTTPException(404, "Colección no encontrada")
        return coleccion
 
    #  CREATE (con transacción)
    
    @staticmethod
    def create_coleccion(dto: ColeccionCreateDTO, db: Session):
        try:
            nuevo = ColeccionRepository.create_coleccion(
                id_usuario=1, # Cambiar dinámicamente cuando integres JWT auth
                nombre=dto.nombre,
                db=db
            )
            db.commit()
            db.refresh(nuevo)
            return nuevo
        except IntegrityError:
            db.rollback()
            raise HTTPException(400, "Error de integridad al crear la colección")
        except Exception:
            db.rollback()
            raise HTTPException(500, "Error interno del servidor")

    # UPDATE (con transacción)
    
    @staticmethod
    def update_coleccion(id_coleccion: int, dto: ColeccionUpdateDTO, db: Session):
        # Validación preventiva fuera del bloque de escritura
        ColeccionService.find_coleccion(id_coleccion, db)
        
        try:
            updated = ColeccionRepository.update_coleccion(
                id_coleccion=id_coleccion,
                dto=dto,
                db=db
            )
            if updated is None:
                raise HTTPException(404, "Colección no encontrada")
            
            db.commit()
            db.refresh(updated)
            return updated
        except IntegrityError:
            db.rollback()
            raise HTTPException(400, "Error de integridad al actualizar la colección")
        except Exception as e:
            db.rollback()
            raise HTTPException(400, f"No se pudo actualizar: {str(e)}")
 
    # DELETE (soft delete, con transacción)
    
    @staticmethod
    def delete_coleccion(id_coleccion: int, db: Session):
        # Validación preventiva fuera del bloque de escritura
        ColeccionService.find_coleccion(id_coleccion, db)
        
        try:
            result = ColeccionRepository.delete_coleccion(id_coleccion, db)
            if result is None:
                raise HTTPException(404, "Colección no encontrada")
            
            db.commit()
            return {"message": "Colección eliminada exitosamente"}
        except Exception as e:
            db.rollback()
            raise HTTPException(400, f"No se pudo eliminar: {str(e)}")
 
    # RESTORE (con transacción)
    
    @staticmethod
    def restore_coleccion(id_coleccion: int, db: Session):
        try:
            result = ColeccionRepository.restore_coleccion(id_coleccion, db)
            if result is None:
                raise HTTPException(404, "Colección no encontrada o ya está activa")
            
            db.commit()
            db.refresh(result)
            return result
        except Exception as e:
            db.rollback()
            raise HTTPException(400, f"No se pudo restaurar: {str(e)}")
