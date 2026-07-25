from sqlalchemy.orm import Session
from src.models.series import Serie

class SerieRepository:
    
    @staticmethod
    def get_series(db: Session):
        """Obtener todas las series"""
        series = db.query(Serie).all()
        return series
    
    @staticmethod
    def find_serie(id_serie: int, db: Session):
        """Buscar una serie por ID"""
        serie = db.query(Serie).filter(Serie.id_serie == id_serie).first()
        return serie
    
    @staticmethod
    def create_serie(data: Serie, db: Session):
        """Crear una nueva serie"""
        db.add(data)
        db.commit()
        db.refresh(data)
        return data
    
    @staticmethod
    def update_serie(id_serie: int, data: dict, db: Session):
        """Actualizar una serie existente"""
        serie = SerieRepository.find_serie(id_serie, db)
        
        if serie is None:
            return None
        
        # Actualizar solo los campos proporcionados
        for key, value in data.items():
            if hasattr(serie, key):
                setattr(serie, key, value)
        
        db.commit()
        db.refresh(serie)
        return serie
    
    @staticmethod
    def delete_serie(id_serie: int, db: Session):
        """Eliminar una serie"""
        serie = SerieRepository.find_serie(id_serie, db)
        
        if serie is None:
            return None
        
        db.delete(serie)
        db.commit()
        return serie