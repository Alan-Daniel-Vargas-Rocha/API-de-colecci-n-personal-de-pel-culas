from sqlalchemy.orm import Session
from src.models.coleccion import Coleccion
from src.models.pelicula import Pelicula

class ColeccionRepository:
    
    @staticmethod
    def get_colecciones(db: Session):
        """Obtener todas las colecciones activas"""
        colecciones = db.query(Coleccion).all()
        return colecciones
    
    @staticmethod
    def find_coleccion(id_coleccion: int, db: Session):
        """Buscar una colección por ID"""
        colecciones = db.query(Coleccion).filter(Coleccion.id_coleccion == id_coleccion).first()
        return colecciones
    
    @staticmethod
    def create_coleccion(data: Coleccion, db: Session):
        """Crear una nueva colección"""
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
        
        # Actualizar solo los campos proporcionados
        for key, value in data.items():
            if hasattr(coleccion, key):
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
    def add_pelicula_to_coleccion(id_coleccion: int, pelicula_id: int, db: Session):
        """Agregar una película a una colección"""
        coleccion = ColeccionRepository.find_coleccion(id_coleccion, db)
        if coleccion is None:
            return None
        
        pelicula = db.query(Pelicula).filter(Pelicula.id_pelicula == pelicula_id).first()
        if pelicula is None:
            return None
        
        # Verificar si la película ya está en la colección
        if pelicula not in coleccion.peliculas:
            coleccion.peliculas.append(pelicula)
            db.commit()
            db.refresh(coleccion)
        
        return coleccion
    
    @staticmethod
    def remove_pelicula_from_coleccion(id_coleccion: int, pelicula_id: int, db: Session):
        """Remover una película de una colección"""
        coleccion = ColeccionRepository.find_coleccion(id_coleccion, db)
        if coleccion is None:
            return None
        
        pelicula = db.query(Pelicula).filter(Pelicula.id == pelicula_id).first()
        if pelicula is None:
            return None
        
        # Remover la película de la colección
        if pelicula in coleccion.peliculas:
            coleccion.peliculas.remove(pelicula)
            db.commit()
            db.refresh(coleccion)
        
        return coleccion