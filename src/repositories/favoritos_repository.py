"""
Repositorio para manejar las operaciones CRUD de favoritos.
"""
from sqlalchemy.orm import Session
from sqlalchemy import and_
from src.models.favoritos import Favorito
from src.models.pelicula import Pelicula
from src.models.series import Serie
from src.utils.logger import setup_logger

logger = setup_logger("favorito_repository")

class FavoritoRepository:
    
    @staticmethod
    def get_favoritos_usuario(id_usuario: int, db: Session):
        """Obtener todos los favoritos de un usuario."""
        logger.debug(f"Obteniendo favoritos del usuario ID: {id_usuario}")
        return db.query(Favorito).filter(
            Favorito.id_usuario == id_usuario
        ).all()
    
    @staticmethod
    def get_favoritos_peliculas(id_usuario: int, db: Session):
        """Obtener favoritos de tipo película de un usuario."""
        logger.debug(f"Obteniendo películas favoritas del usuario ID: {id_usuario}")
        return db.query(Favorito).filter(
            Favorito.id_usuario == id_usuario,
            Favorito.tipo == "pelicula"
        ).all()
    
    @staticmethod
    def get_favoritos_series(id_usuario: int, db: Session):
        """Obtener favoritos de tipo serie de un usuario."""
        logger.debug(f"Obteniendo series favoritas del usuario ID: {id_usuario}")
        return db.query(Favorito).filter(
            Favorito.id_usuario == id_usuario,
            Favorito.tipo == "serie"
        ).all()
    
    @staticmethod
    def find_favorito(id_usuario: int, tipo: str, id_item: int, db: Session):
        """Buscar un favorito específico."""
        logger.debug(f"Buscando favorito: usuario={id_usuario}, tipo={tipo}, item={id_item}")
        return db.query(Favorito).filter(
            Favorito.id_usuario == id_usuario,
            Favorito.tipo == tipo,
            Favorito.id_item == id_item
        ).first()
    
    @staticmethod
    def find_favorito_by_id(id_favorito: int, db: Session):
        """Buscar un favorito por su ID."""
        logger.debug(f"Buscando favorito ID: {id_favorito}")
        return db.query(Favorito).filter(
            Favorito.id_favorito == id_favorito
        ).first()
    
    @staticmethod
    def create_favorito(data: Favorito, db: Session):
        """Crear un nuevo favorito."""
        logger.info(f"Creando favorito: usuario={data.id_usuario}, tipo={data.tipo}, item={data.id_item}")
        db.add(data)
        db.commit()
        db.refresh(data)
        logger.info(f"Favorito creado: ID={data.id_favorito}")
        return data
    
    @staticmethod
    def delete_favorito(id_favorito: int, db: Session):
        """Eliminar un favorito."""
        logger.warning(f"Eliminando favorito ID: {id_favorito}")
        
        favorito = FavoritoRepository.find_favorito_by_id(id_favorito, db)
        if favorito is None:
            logger.warning(f"Favorito no encontrado: ID={id_favorito}")
            return None
        
        db.delete(favorito)
        db.commit()
        logger.warning(f"Favorito eliminado: ID={id_favorito}")
        return favorito
    
    @staticmethod
    def delete_favorito_by_item(id_usuario: int, tipo: str, id_item: int, db: Session):
        """Eliminar un favorito por usuario, tipo e item."""
        logger.warning(f"Eliminando favorito: usuario={id_usuario}, tipo={tipo}, item={id_item}")
        
        favorito = FavoritoRepository.find_favorito(id_usuario, tipo, id_item, db)
        if favorito is None:
            logger.warning(f"Favorito no encontrado: usuario={id_usuario}, tipo={tipo}, item={id_item}")
            return None
        
        db.delete(favorito)
        db.commit()
        logger.warning(f"Favorito eliminado: usuario={id_usuario}, tipo={tipo}, item={id_item}")
        return favorito