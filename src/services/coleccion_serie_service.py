from fastapi import HTTPException
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session
from src.dtos.coleccionserie.coleccion_serie_create import ColeccionSerieCreateDTO
from src.dtos.coleccionserie.coleccion_serie_update import ColeccionSerieUpdateDTO
from src.repositories.coleccion_series_repository import ColeccionSerieRepository

class ColeccionSerieService:
    
    @staticmethod
    def get_all_colecciones_series(db: Session):
        """Obtener todas las relaciones colección-serie (global)"""
        return ColeccionSerieRepository.get_all_colecciones_series(db=db)
    
    @staticmethod
    def get_series_from_coleccion(id_coleccion: int, db: Session):
        return ColeccionSerieRepository.get_series_from_coleccion(id_coleccion, db)
    
    @staticmethod
    def find_coleccion_serie(id_coleccion: int, id_serie: int, db: Session):
        coleccion_serie = ColeccionSerieRepository.find_coleccion_serie(
            id_coleccion, id_serie, db
        )
        if not coleccion_serie:
            raise HTTPException(404, "Relación colección-serie no encontrada")
        return coleccion_serie
    
    @staticmethod
    def add_serie_to_coleccion(
        id_coleccion: int,
        id_serie: int,
        dto: ColeccionSerieCreateDTO,
        db: Session
    ):
        # Validación preventiva fuera del bloque de escritura
        existe = ColeccionSerieRepository.find_coleccion_serie(id_coleccion, id_serie, db)
        if existe:
            raise HTTPException(400, "Esta serie ya está en la colección")
        
        try:
            nuevo = ColeccionSerieRepository.add_serie_to_coleccion(
                id_coleccion=id_coleccion,
                id_serie=id_serie,
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
    def update_serie_in_coleccion(
        id_coleccion: int,
        id_serie: int,
        dto: ColeccionSerieUpdateDTO,
        db: Session
    ):
        """Actualizar una relación colección-serie"""
        ColeccionSerieService.find_coleccion_serie(id_coleccion, id_serie, db)
        
        try:
            updated = ColeccionSerieRepository.update_serie_in_coleccion(
                id_coleccion=id_coleccion,
                id_serie=id_serie,
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
    def delete_coleccion_serie(id_coleccion: int, id_serie: int, db: Session):
        """ Escritura: con transacción"""
        ColeccionSerieService.find_coleccion_serie(id_coleccion, id_serie, db)
        
        try:
            result = ColeccionSerieRepository.delete_coleccion_serie(
                id_coleccion, id_serie, db
            )
            if result is None:
                raise HTTPException(404, "Relación no encontrada")
            
            db.commit()
            return {"message": "Serie removida exitosamente"}
        except Exception as e:
            db.rollback()
            raise HTTPException(400, f"No se pudo eliminar: {str(e)}")
