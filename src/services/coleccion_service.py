from fastapi import HTTPException
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session
from src.dtos.coleccion.coleccion_create import ColeccionCreateDTO
from src.dtos.coleccion.coleccion_update import ColeccionUpdateDTO
from src.repositories.coleccion_repository import ColeccionRepository
from src.repositories.coleccion_pelicula_repository import ColeccionPeliculaRepository
from src.repositories.coleccion_series_repository import ColeccionSerieRepository

class ColeccionService:
 
    # ============================================
    # 1️⃣ LECTURAS
    # ============================================
    
    @staticmethod
    def get_colecciones(db: Session):
        return ColeccionRepository.get_colecciones(db=db)
    
    @staticmethod
    def find_coleccion(id_coleccion: int, db: Session):
        coleccion = ColeccionRepository.find_coleccion(id_coleccion, db)
        if not coleccion:
            raise HTTPException(404, "Colección no encontrada")
        return coleccion
 
    # ============================================
    # 2️⃣ CREATE
    # ============================================
    
    @staticmethod
    def create_coleccion(dto: ColeccionCreateDTO, db: Session):
        try:
            nuevo = ColeccionRepository.create_coleccion(
                id_usuario=1,
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

    # ============================================
    # 3️⃣ UPDATE
    # ============================================
    
    @staticmethod
    def update_coleccion(id_coleccion: int, dto: ColeccionUpdateDTO, db: Session):
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
 
    # ============================================
    # 4️⃣ DELETE
    # ============================================
    
    @staticmethod
    def delete_coleccion(id_coleccion: int, db: Session):
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
 
    # ============================================
    # 5️⃣ RESTORE
    # ============================================
    
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

    # ============================================
    # 6️⃣ PELÍCULAS
    # ============================================
    
    @staticmethod
    def add_pelicula_to_coleccion(id_coleccion: int, id_pelicula: int, db: Session):
        # 1️⃣ Verificar que la colección existe
        coleccion = ColeccionRepository.find_coleccion(id_coleccion, db)
        if not coleccion:
            raise HTTPException(404, "Colección no encontrada")
        
        # 2️⃣ Verificar que la película existe
        from src.repositories.pelicula_repository import PeliculaRepository
        pelicula = PeliculaRepository.find_pelicula(id_pelicula, db)
        if not pelicula:
            raise HTTPException(404, "Película no encontrada en el catálogo")
        
        # 3️⃣ Verificar si la película ya está en la colección
        from src.repositories.coleccion_pelicula_repository import ColeccionPeliculaRepository
        existe = ColeccionPeliculaRepository.find_coleccion_pelicula(id_coleccion, id_pelicula, db)
        if existe:
            raise HTTPException(400, "Esta película ya está en la colección")
        
        # 4️⃣ Crear la relación
        try:
            from src.dtos.coleccion_pelicula.coleccion_pelicula_create import ColeccionPeliculaCreateDTO
            dto = ColeccionPeliculaCreateDTO(
                id_coleccion=id_coleccion,
                id_pelicula=id_pelicula
            )
            resultado = ColeccionPeliculaRepository.create_coleccion_pelicula(dto, db)
            db.commit()
            db.refresh(resultado)
            return resultado
        except IntegrityError:
            db.rollback()
            raise HTTPException(400, "La película ya está en la colección (error de integridad)")
        except Exception as e:
            db.rollback()
            raise HTTPException(400, f"Error al agregar la película: {str(e)}")
    
    @staticmethod
    def remove_pelicula_from_coleccion(id_coleccion: int, id_pelicula: int, db: Session):
        # Verificar que la colección existe
        ColeccionService.find_coleccion(id_coleccion, db)
        
        try:
            resultado = ColeccionPeliculaRepository.delete_coleccion_pelicula(id_coleccion, id_pelicula, db)
            if resultado is None:
                raise HTTPException(404, "La película no está en esta colección")
            
            db.commit()
            return {"message": "Película removida de la colección"}
        except Exception as e:
            db.rollback()
            raise HTTPException(400, f"No se pudo remover la película: {str(e)}")

    # ============================================
    # 7️⃣ SERIES
    # ============================================
    
    @staticmethod
    def add_serie_to_coleccion(id_coleccion: int, id_serie: int, db: Session):
        # Verificar que la colección existe
        ColeccionService.find_coleccion(id_coleccion, db)
        
        try:
            from src.dtos.coleccionserie.coleccion_serie_create import ColeccionSerieCreateDTO
            dto = ColeccionSerieCreateDTO(
                id_coleccion=id_coleccion,
                id_serie=id_serie
            )
            resultado = ColeccionSerieRepository.add_serie_to_coleccion(dto, db)
            db.commit()
            db.refresh(resultado)
            return resultado
        except IntegrityError:
            db.rollback()
            raise HTTPException(400, "La serie ya está en la colección")
        except Exception as e:
            db.rollback()
            raise HTTPException(400, f"No se pudo agregar la serie: {str(e)}")
    
    @staticmethod
    def remove_serie_from_coleccion(id_coleccion: int, id_serie: int, db: Session):
        # Verificar que la colección existe
        ColeccionService.find_coleccion(id_coleccion, db)
        
        try:
            resultado = ColeccionSerieRepository.remove_serie_from_coleccion(id_coleccion, id_serie, db)
            if resultado is None:
                raise HTTPException(404, "La serie no está en esta colección")
            
            db.commit()
            return {"message": "Serie removida de la colección"}
        except Exception as e:
            db.rollback()
            raise HTTPException(400, f"No se pudo remover la serie: {str(e)}")