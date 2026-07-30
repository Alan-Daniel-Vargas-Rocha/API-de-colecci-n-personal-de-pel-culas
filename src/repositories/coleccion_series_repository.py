from sqlalchemy.orm import Session
from src.models.coleccionserie import ColeccionSerie
from src.models.coleccion import Coleccion
from src.models.series import Serie

class ColeccionSerieRepository:
    
    @staticmethod
    def get_series_from_coleccion(id_coleccion: int, db: Session):
        """Obtener todas las series de una colección"""
        coleccion_series = db.query(ColeccionSerie).filter(
            ColeccionSerie.id_coleccion == id_coleccion
        ).all()
        return coleccion_series
    
    @staticmethod
    def find_coleccion_serie(id_coleccion: int, id_serie: int, db: Session):  
        """Buscar una relación colección-serie específica"""
        coleccion_serie = db.query(ColeccionSerie).filter(
            ColeccionSerie.id_coleccion == id_coleccion,
            ColeccionSerie.id_serie == id_serie  
        ).first()
        return coleccion_serie
    
    @staticmethod
    def add_serie_to_coleccion(id_coleccion: int, id_serie: int, data: dict, db: Session):  
        """Agregar una serie a una colección"""
        # Verificar que la colección existe
        coleccion = db.query(Coleccion).filter(Coleccion.id_coleccion == id_coleccion).first()
        if coleccion is None:
            return None
        
        # Verificar que la serie existe
        serie = db.query(Serie).filter(Serie.id_serie == id_serie).first()  
        if serie is None:
            return None
        
        # Verificar si la serie ya está en la colección
        existing = db.query(ColeccionSerie).filter(
            ColeccionSerie.id_coleccion == id_coleccion,
            ColeccionSerie.id_serie == id_serie  
        ).first()
        
        if existing is not None:
            return existing
        
        # Crear la relación
        coleccion_serie = ColeccionSerie(
            id_coleccion=id_coleccion,
            id_serie=id_serie,
            opinion=data.get('opinion'),
            calificacion=data.get('calificacion'),
            nombre_personalizado=data.get('nombre_personalizado')
        )
        
        db.add(coleccion_serie)
        db.commit()
        db.refresh(coleccion_serie)
        return coleccion_serie
    
    @staticmethod
    def update_serie_in_coleccion(id_coleccion: int, id_serie: int, data: dict, db: Session):  
        """Actualizar la relación colección-serie (opinión y calificación)"""
        coleccion_serie = ColeccionSerieRepository.find_coleccion_serie(id_coleccion, id_serie, db)  
        
        if coleccion_serie is None:
            return None
        
        # Actualizar solo los campos proporcionados
        for key, value in data.items():
            if hasattr(coleccion_serie, key):
                setattr(coleccion_serie, key, value)
        
        db.commit()
        db.refresh(coleccion_serie)
        return coleccion_serie
    
    @staticmethod
    def remove_serie_from_coleccion(id_coleccion: int, id_serie: int, db: Session):  
        """Remover una serie de una colección"""
        coleccion_serie = ColeccionSerieRepository.find_coleccion_serie(id_coleccion, id_serie, db)  
        
        if coleccion_serie is None:
            return None
        
        db.delete(coleccion_serie)
        db.commit()
        return coleccion_serie
    
    @staticmethod
    def get_serie_details_from_coleccion(id_coleccion: int, id_serie: int, db: Session):  
        """Obtener detalles de una serie específica en una colección"""
        coleccion_serie = ColeccionSerieRepository.find_coleccion_serie(id_coleccion, id_serie, db)  
        
        if coleccion_serie is None:
            return None
        
        # También obtener la información de la serie
        serie = db.query(Serie).filter(Serie.id_serie == id_serie).first()  
        
        return {
            "coleccion_serie": coleccion_serie,
            "serie": serie
        }