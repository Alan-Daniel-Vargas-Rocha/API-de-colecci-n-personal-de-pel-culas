"""
Repositorio para manejar las operaciones CRUD de la relación colección-película.

Provee métodos para:
- Obtener todas las relaciones
- Buscar una relación específica
- Crear, actualizar y eliminar relaciones
"""
from sqlalchemy.orm import Session
from src.models.coleccion_pelicula import ColeccionPelicula
from datetime import datetime, timezone

class ColeccionPeliculaRepository:
    
    @staticmethod
    def get_colecciones_peliculas(db: Session):
        """
        Obtiene todas las relaciones colección-película.
        
        Args:
            db (Session): Sesión de SQLAlchemy
            
        Returns:
            List[ColeccionPelicula]: Lista de todas las relaciones
        """
        return db.query(ColeccionPelicula).all()
    
    @staticmethod
    def find_coleccion_pelicula(id_coleccion: int, id_pelicula: int, db: Session):
        """
        Busca una relación colección-película específica.
        
        Args:
            id_coleccion (int): ID de la colección
            id_pelicula (int): ID de la película
            db (Session): Sesión de SQLAlchemy
            
        Returns:
            ColeccionPelicula: La relación encontrada o None
        """
        coleccion_pelicula = db.query(ColeccionPelicula).filter(
            ColeccionPelicula.id_coleccion == id_coleccion,
            ColeccionPelicula.id_pelicula == id_pelicula
        ).first()
        return coleccion_pelicula
    
    @staticmethod
    def create_coleccion_pelicula(data: ColeccionPelicula, db: Session):
        """
        Crea una nueva relación colección-película.
        
        Args:
            data (ColeccionPelicula): Datos de la relación a crear
            db (Session): Sesión de SQLAlchemy
            
        Returns:
            ColeccionPelicula: La relación creada
        """
        db.add(data)
        db.commit()
        db.refresh(data)
        return data
    
    @staticmethod
    def update_coleccion_pelicula(
        id_coleccion: int, 
        id_pelicula: int, 
        update_data: dict, 
        db: Session
    ):
        """
        Actualiza una relación colección-película existente.
        
        Args:
            id_coleccion (int): ID de la colección
            id_pelicula (int): ID de la película
            update_data (dict): Diccionario con los campos a actualizar
            db (Session): Sesión de SQLAlchemy
            
        Returns:
            ColeccionPelicula: La relación actualizada o None
        """
        # Buscar la relación
        coleccion_pelicula = ColeccionPeliculaRepository.find_coleccion_pelicula(
            id_coleccion=id_coleccion,
            id_pelicula=id_pelicula,
            db=db
        )
        
        if coleccion_pelicula is None:
            return None
        
        # Actualizar solo los campos proporcionados
        for key, value in update_data.items():
            if hasattr(coleccion_pelicula, key):
                setattr(coleccion_pelicula, key, value)
        
        # Actualizar timestamp automáticamente
        coleccion_pelicula.coleccion_pelicula_update_at = datetime.now(timezone.utc)
        
        db.commit()
        db.refresh(coleccion_pelicula)
        return coleccion_pelicula
    
    @staticmethod
    def delete_coleccion_pelicula(id_coleccion: int, id_pelicula: int, db: Session):
        """
        Elimina una relación colección-película.
        
        Args:
            id_coleccion (int): ID de la colección
            id_pelicula (int): ID de la película
            db (Session): Sesión de SQLAlchemy
            
        Returns:
            ColeccionPelicula: La relación eliminada o None
        """
        coleccion_pelicula = ColeccionPeliculaRepository.find_coleccion_pelicula(
            id_coleccion=id_coleccion,
            id_pelicula=id_pelicula,
            db=db
        )
        
        if coleccion_pelicula is None:
            return None
        
        db.delete(coleccion_pelicula)
        db.commit()
        return coleccion_pelicula