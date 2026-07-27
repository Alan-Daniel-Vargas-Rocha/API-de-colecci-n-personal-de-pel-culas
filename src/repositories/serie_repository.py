from sqlalchemy.orm import Session
from src.models.series import Serie
from src.utils.logger import setup_logger

logger = setup_logger("serie_repository")

class SerieRepository:
    
    @staticmethod
    def get_series(db: Session):
        """Obtener todas las series del catálogo."""
        logger.debug("Obteniendo todas las series")
        return db.query(Serie).all()
    
    @staticmethod
    def find_serie(id_serie: int, db: Session):
        """Buscar una serie por ID."""
        logger.debug(f"Buscando serie con ID: {id_serie}")
        return db.query(Serie).filter(Serie.id_serie == id_serie).first()
    
    @staticmethod
    def create_serie(data: Serie, db: Session):
        """Crear una nueva serie en el catálogo."""
        logger.info(f"Creando serie: {data.titulo}")
        db.add(data)
        db.commit()
        db.refresh(data)
        logger.info(f"Serie creada: ID={data.id_serie}")
        return data
    
    @staticmethod
    def update_serie(id_serie: int, update_data: dict, db: Session):
        """Actualizar una serie existente."""
        logger.info(f"Actualizando serie ID: {id_serie}")
        
        serie = SerieRepository.find_serie(id_serie, db)
        if serie is None:
            logger.warning(f"Serie no encontrada: ID={id_serie}")
            return None
        
        for key, value in update_data.items():
            if hasattr(serie, key):
                setattr(serie, key, value)
                logger.debug(f"Campo actualizado: {key} = {value}")
        
        db.commit()
        db.refresh(serie)
        logger.info(f"Serie actualizada: ID={id_serie}")
        return serie
    
    @staticmethod
    def delete_serie(id_serie: int, db: Session):
        """Eliminar una serie del catálogo."""
        logger.warning(f"Eliminando serie ID: {id_serie}")
        
        serie = SerieRepository.find_serie(id_serie, db)
        if serie is None:
            logger.warning(f"Serie no encontrada: ID={id_serie}")
            return None
        
        db.delete(serie)
        db.commit()
        logger.warning(f"Serie eliminada: ID={id_serie}")
        return serie