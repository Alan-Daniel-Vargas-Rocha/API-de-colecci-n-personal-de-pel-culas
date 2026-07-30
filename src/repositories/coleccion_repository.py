from sqlalchemy.orm import Session
from src.models.coleccion import Coleccion
from src.models.pelicula import Pelicula
from src.models.series import Serie
from src.models.coleccion_pelicula import ColeccionPelicula
from src.models.coleccionserie import ColeccionSerie
from datetime import datetime, timezone

class ColeccionRepository:
    
    @staticmethod
    def get_colecciones(db: Session):
        """Obtener todas las colecciones activas"""
        colecciones = db.query(Coleccion).filter(Coleccion.activo == True).all()
        return colecciones
    
    @staticmethod
    def find_coleccion(id_coleccion: int, db: Session):
        """Buscar una colección activa por ID"""
        coleccion = db.query(Coleccion).filter(
            Coleccion.id_coleccion == id_coleccion,
            Coleccion.activo == True
        ).first()
        return coleccion
    
    @staticmethod
    def find_coleccion_including_inactive(id_coleccion: int, db: Session):
        """Buscar una colección por ID (incluyendo inactivas)"""
        coleccion = db.query(Coleccion).filter(
            Coleccion.id_coleccion == id_coleccion
        ).first()
        return coleccion
    
    @staticmethod
    def create_coleccion(data: Coleccion, db: Session):
        """Crear una nueva colección"""
        data.activo = True
        db.add(data)
        db.commit()
        db.refresh(data)
        return data
    
    @staticmethod
    def update_coleccion(id_coleccion: int, data: dict, db: Session):
        """Actualizar una colección existente"""
        coleccion = ColeccionRepository.find_coleccion(id_coleccion, db)
        
        if coleccion is None:
            return None
        
        for key, value in data.items():
            if hasattr(coleccion, key) and key != 'activo':
                setattr(coleccion, key, value)
        
        db.commit()
        db.refresh(coleccion)
        return coleccion
    
    @staticmethod
    def delete_coleccion(id_coleccion: int, db: Session):
        """Soft delete - marcar como inactiva"""
        coleccion = ColeccionRepository.find_coleccion(id_coleccion, db)
        
        if coleccion is None:
            return None
        
        coleccion.activo = False
        db.commit()
        db.refresh(coleccion)
        return coleccion
    
    @staticmethod
    def restore_coleccion(id_coleccion: int, db: Session):
        """Restaurar una colección eliminada"""
        coleccion = ColeccionRepository.find_coleccion_including_inactive(id_coleccion, db)
        
        if coleccion is None or coleccion.activo == True:
            return None
        
        coleccion.activo = True
        db.commit()
        db.refresh(coleccion)
        return coleccion
    
    # ============ MÉTODOS PARA PELÍCULAS ============
    
    @staticmethod
    def add_pelicula_to_coleccion(id_coleccion: int, pelicula_id: int, db: Session):
        """Agregar una película a una colección"""
        coleccion = ColeccionRepository.find_coleccion(id_coleccion, db)
        if coleccion is None:
            return None
        
        pelicula = db.query(Pelicula).filter(Pelicula.id_pelicula == pelicula_id).first()
        if pelicula is None:
            return None
        
        # Verificar si la película ya está en la colección
        for cp in coleccion.coleccion_peliculas:
            if cp.pelicula_id == pelicula_id:
                return coleccion  # Ya existe, no hacer nada
        
        # Crear la relación en la tabla intermedia
        nueva_relacion = ColeccionPelicula(
            pelicula_id=pelicula_id,
            id_coleccion=id_coleccion,
            fecha_agregado=datetime.now(timezone.utc),
            coleccion_pelicula_created_at=datetime.now(timezone.utc),
            coleccion_pelicula_update_at=datetime.now(timezone.utc)
        )
        
        db.add(nueva_relacion)
        db.commit()
        db.refresh(coleccion)
        
        return coleccion
    
    @staticmethod
    def remove_pelicula_from_coleccion(id_coleccion: int, pelicula_id: int, db: Session):
        """Remover una película de una colección"""
        coleccion = ColeccionRepository.find_coleccion(id_coleccion, db)
        if coleccion is None:
            return None
        
        # Buscar la relación en la tabla intermedia
        relacion_a_eliminar = None
        for cp in coleccion.coleccion_peliculas:
            if cp.pelicula_id == pelicula_id:
                relacion_a_eliminar = cp
                break
        
        if relacion_a_eliminar is None:
            return coleccion  # No existe, no hacer nada
        
        db.delete(relacion_a_eliminar)
        db.commit()
        db.refresh(coleccion)
        
        return coleccion
    
    # ============ MÉTODOS PARA SERIES ============
    
    @staticmethod
    def add_serie_to_coleccion(id_coleccion: int, id_serie: int, db: Session):
        """Agregar una serie a una colección"""
        coleccion = ColeccionRepository.find_coleccion(id_coleccion, db)
        if coleccion is None:
            return None
        
        serie = db.query(Serie).filter(Serie.id_serie == id_serie).first()
        if serie is None:
            return None
        
        # Verificar si la serie ya está en la colección
        for cs in coleccion.coleccion_series:
            if cs.id_serie == id_serie:
                return coleccion  # Ya existe, no hacer nada
        
        # Crear la relación en la tabla intermedia
        nueva_relacion = ColeccionSerie(
            id_serie=id_serie,
            id_coleccion=id_coleccion,
            fecha_agregado=datetime.now(timezone.utc),
            coleccion_serie_created_at=datetime.now(timezone.utc),
            coleccion_serie_update_at=datetime.now(timezone.utc)
        )
        
        db.add(nueva_relacion)
        db.commit()
        db.refresh(coleccion)
        
        return coleccion
    
    @staticmethod
    def remove_serie_from_coleccion(id_coleccion: int, id_serie: int, db: Session):
        """Remover una serie de una colección"""
        coleccion = ColeccionRepository.find_coleccion(id_coleccion, db)
        if coleccion is None:
            return None
        
        # Buscar la relación en la tabla intermedia
        relacion_a_eliminar = None
        for cs in coleccion.coleccion_series:
            if cs.id_serie == id_serie:
                relacion_a_eliminar = cs
                break
        
        if relacion_a_eliminar is None:
            return coleccion  # No existe, no hacer nada
        
        db.delete(relacion_a_eliminar)
        db.commit()
        db.refresh(coleccion)
        
        return coleccion