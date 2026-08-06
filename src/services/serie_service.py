from fastapi import HTTPException
from sqlalchemy.exc import IntegrityError
from starlette import status
from sqlalchemy.orm import Session
from datetime import datetime, timezone

from src.dtos.series.series_create import SerieCreateDTO
from src.dtos.series.series_update import SerieUpdateDTO
from src.repositories.serie_repository import SerieRepository

class SerieService:
    
    # ============================================
    # 1️⃣ LECTURAS (sin transacción)
    # ============================================
    
    @staticmethod
    def get_series(db: Session):
        return SerieRepository.get_series(db=db)
    
    @staticmethod
    def find_serie(id_serie: int, db: Session):
        serie = SerieRepository.find_serie(id_serie, db)
        
        if not serie:
            raise HTTPException(404, "Serie no encontrada")
        
        return serie
    
    # ============================================
    # 2️⃣ CREATE (con transacción)
    # ============================================
    
    @staticmethod
    def create_serie(dto: SerieCreateDTO, db: Session):
        # 1. Validaciones de negocio (pre-transacción)
        if not dto.titulo or len(dto.titulo.strip()) == 0:
            raise HTTPException(400, "El título es obligatorio")
        
        if len(dto.titulo) > 32:
            raise HTTPException(400, "El título excede los 32 caracteres")
        
        if not dto.genero or len(dto.genero.strip()) == 0:
            raise HTTPException(400, "El género es obligatorio")
        
        if len(dto.genero) > 30:
            raise HTTPException(400, "El género excede los 30 caracteres")
        
        if dto.año_inicio and dto.año_fin and dto.año_inicio > dto.año_fin:
            raise HTTPException(400, "El año de inicio no puede ser mayor que el año de fin")
        
        # 2. Control de transacción
        try:
            # ✅ Delegar al repositorio
            nueva = SerieRepository.create_serie(dto, db)
            
            # ✅ Confirmar transacción
            db.commit()
            db.refresh(nueva)
            return nueva
            
        except IntegrityError:
            db.rollback()
            raise HTTPException(400, "Error de integridad: la serie ya existe o los datos son inválidos")
        except HTTPException:
            raise
        except Exception as e:
            db.rollback()
            raise HTTPException(500, f"Error interno del servidor: {str(e)}")
    
    # ============================================
    # 3️⃣ UPDATE (con transacción)
    # ============================================
    
    @staticmethod
    def update_serie(id_serie: int, dto: SerieUpdateDTO, db: Session):
        try:
            # ✅ Verificar que existe
            SerieService.find_serie(id_serie, db)
            
            # ✅ Validaciones de negocio
            if dto.año_inicio is not None and dto.año_fin is not None and dto.año_inicio > dto.año_fin:
                raise HTTPException(400, "El año de inicio no puede ser mayor que el año de fin")
            
            # ✅ Delegar al repositorio
            updated = SerieRepository.update_serie(
                id_serie=id_serie,
                dto=dto,
                db=db
            )
            
            if updated is None:
                raise HTTPException(404, "Serie no encontrada")
            
            # ✅ Confirmar transacción
            db.commit()
            db.refresh(updated)
            return updated
            
        except HTTPException:
            raise
        except IntegrityError:
            db.rollback()
            raise HTTPException(400, "Error de integridad al actualizar la serie")
        except Exception as e:
            db.rollback()
            raise HTTPException(400, f"No se pudo actualizar la serie: {str(e)}")
    
    # ============================================
    # 4️⃣ DELETE (soft delete, con transacción)
    # ============================================
    
    @staticmethod
    def delete_serie(id_serie: int, db: Session):
        try:
            # ✅ Verificar que existe
            SerieService.find_serie(id_serie, db)
            
            # ✅ Delegar al repositorio
            result = SerieRepository.delete_serie(id_serie, db)
            
            if result is None:
                raise HTTPException(404, "Serie no encontrada")
            
            # ✅ Confirmar transacción
            db.commit()
            return {"message": "Serie eliminada exitosamente"}
            
        except HTTPException:
            raise
        except Exception as e:
            db.rollback()
            raise HTTPException(400, f"No se pudo eliminar la serie: {str(e)}")
    
    # ============================================
    # 5️⃣ RESTORE (con transacción)
    # ============================================
    
    @staticmethod
    def restore_serie(id_serie: int, db: Session):
        try:
            result = SerieRepository.restore_serie(id_serie, db)
            if result is None:
                raise HTTPException(404, "Serie no encontrada o ya está activa")
            db.commit()
            db.refresh(result)
            return result
        except Exception as e:
            db.rollback()
            raise HTTPException(400, f"No se pudo restaurar la serie: {str(e)}")