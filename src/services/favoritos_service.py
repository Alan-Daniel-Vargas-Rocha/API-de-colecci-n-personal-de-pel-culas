from fastapi import HTTPException
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from src.dtos.favoritos.favoritos_create import FavoritoCreateDTO
from src.repositories.favoritos_repository import FavoritoRepository
from src.repositories.pelicula_repository import PeliculaRepository
from src.repositories.serie_repository import SerieRepository
from src.services.usuario_service import UsuarioService
from src.utils.logger import setup_logger

logger = setup_logger("favorito_service")

class FavoritoService:
    
    # LECTURAS (sin transacción)
    
    @staticmethod
    def get_favoritos_usuario(id_usuario: int, db: Session):
        logger.info(f"Obteniendo favoritos del usuario ID: {id_usuario}")
        UsuarioService.find_usuario(id_usuario, db)
        return FavoritoRepository.get_favoritos_usuario(id_usuario, db)
    
    @staticmethod
    def get_favoritos_usuario_amigable(id_usuario: int, db: Session):
        logger.info(f"Obteniendo favoritos amigables del usuario ID: {id_usuario}")
        UsuarioService.find_usuario(id_usuario, db)
        return FavoritoRepository.get_favoritos_usuario_amigable(id_usuario, db)
    
    # CREATE (con transacción)
    
    @staticmethod
    def add_favorito(dto: FavoritoCreateDTO, db: Session):
        logger.info(f"Agregando favorito: usuario={dto.id_usuario}, tipo={dto.tipo}, item={dto.id_item}")
        
        # Validaciones de negocio preventivas
        UsuarioService.find_usuario(dto.id_usuario, db)
        
        if dto.tipo not in ["pelicula", "serie"]:
            raise HTTPException(400, "Tipo inválido. Debe ser 'pelicula' o 'serie'")
        
        if dto.tipo == "pelicula":
            pelicula = PeliculaRepository.find_pelicula(dto.id_item, db)
            if not pelicula:
                raise HTTPException(404, "Película no encontrada")
        else:
            serie = SerieRepository.find_serie(dto.id_item, db)
            if not serie:
                raise HTTPException(404, "Serie no encontrada")
        
        existing = FavoritoRepository.find_favorito(dto.id_usuario, dto.tipo, dto.id_item, db)
        if existing:
            logger.warning(f"El favorito ya existe: usuario={dto.id_usuario}, tipo={dto.tipo}, item={dto.id_item}")
            raise HTTPException(400, "Este item ya está en favoritos")
        
        try:
            nuevo = FavoritoRepository.create_favorito(dto, db)
            db.commit()
            db.refresh(nuevo)
            logger.info(f"Favorito agregado: ID={nuevo.id_favorito}")
            return nuevo
        except IntegrityError:
            db.rollback()
            raise HTTPException(400, "Error de integridad: el favorito ya existe o los datos son inválidos")
        except Exception as e:
            db.rollback()
            logger.error(f"Error al agregar favorito: {str(e)}")
            raise HTTPException(500, f"Error interno del servidor")
    
    #  DELETE BY ID (con transacción)
    
    @staticmethod
    def delete_favorito(id_favorito: int, db: Session):
        logger.warning(f"Intentando eliminar favorito ID: {id_favorito}")
        
        existing = FavoritoRepository.find_favorito_by_id(id_favorito, db)
        if not existing:
            raise HTTPException(404, "Favorito no encontrado")
        
        try:
            result = FavoritoRepository.delete_favorito(id_favorito, db)
            if result is None:
                raise HTTPException(404, "Favorito no encontrado")
            
            db.commit()
            logger.info(f"Favorito eliminado físicamente: ID={id_favorito}")
            return {"message": "Favorito eliminado exitosamente"}
        except Exception as e:
            db.rollback()
            logger.error(f"Error al eliminar favorito ID={id_favorito}: {str(e)}")
            raise HTTPException(500, f"Error interno del servidor")

    # DELETE BY ITEM (con transacción)
    
    @staticmethod
    def delete_favorito_by_item(id_usuario: int, tipo: str, id_item: int, db: Session):
        logger.warning(f"Intentando eliminar favorito: usuario={id_usuario}, tipo={tipo}, item={id_item}")
        
        UsuarioService.find_usuario(id_usuario, db)
        
        if tipo not in ["pelicula", "serie"]:
            raise HTTPException(400, "Tipo inválido. Debe ser 'pelicula' o 'serie'")
            
        existing = FavoritoRepository.find_favorito(id_usuario, tipo, id_item, db)
        if not existing:
            raise HTTPException(404, "El item especificado no se encuentra en tus favoritos")
        
        try:
            FavoritoRepository.delete_favorito_by_item(id_usuario, tipo, id_item, db)
            db.commit()
            logger.info(f"Favorito eliminado: usuario={id_usuario}, tipo={tipo}, item={id_item}")
            return {"message": "Favorito eliminado exitosamente"}
        except Exception as e:
            db.rollback()
            logger.error(f"Error al eliminar favorito: usuario={id_usuario}, {str(e)}")
            raise HTTPException(500, f"Error interno del servidor")
from fastapi import HTTPException
from sqlalchemy.exc import IntegrityError
from starlette import status
from sqlalchemy.orm import Session
from datetime import datetime, timezone

from src.dtos.pelicula.pelicula_created import PeliculaCreateDTO
from src.dtos.pelicula.pelicula_update import PeliculaUpdateDTO
from src.repositories.pelicula_repository import PeliculaRepository

class PeliculaService:
    
    #  LECTURAS (sin transacción)
    
    @staticmethod
    def get_peliculas(db: Session):
        return PeliculaRepository.get_peliculas(db=db)
    
    @staticmethod
    def find_pelicula(id_pelicula: int, db: Session):
        pelicula = PeliculaRepository.find_pelicula(id_pelicula, db)
        
        if not pelicula:
            raise HTTPException(404, "Película no encontrada")
        
        return pelicula
    
    #  CREATE (con transacción)
    
    @staticmethod
    def create_pelicula(dto: PeliculaCreateDTO, db: Session):
        # 1. Validaciones de negocio (pre-transacción)
        if not dto.titulo or len(dto.titulo.strip()) == 0:
            raise HTTPException(400, "El título es obligatorio")
        
        if len(dto.titulo) > 32:
            raise HTTPException(400, "El título excede los 32 caracteres")
        
        if not dto.genero or len(dto.genero.strip()) == 0:
            raise HTTPException(400, "El género es obligatorio")
        
        if len(dto.genero) > 30:
            raise HTTPException(400, "El género excede los 30 caracteres")
        
        # 2. Control de transacción
        try:
            # Delegar al repositorio
            nueva = PeliculaRepository.create_pelicula(dto, db)
            
            # Confirmar transacción
            db.commit()
            db.refresh(nueva)
            return nueva
            
        except IntegrityError:
            db.rollback()
            raise HTTPException(400, "Error de integridad: la película ya existe o los datos son inválidos")
        except HTTPException:
            raise
        except Exception as e:
            db.rollback()
            raise HTTPException(500, f"Error interno del servidor: {str(e)}")
    
    #  UPDATE (con transacción)
    
    @staticmethod
    def update_pelicula(id_pelicula: int, dto: PeliculaUpdateDTO, db: Session):
        try:
            # Verificar que existe
            PeliculaService.find_pelicula(id_pelicula, db)
            
            # Delegar al repositorio
            updated = PeliculaRepository.update_pelicula(
                id_pelicula=id_pelicula,
                dto=dto,
                db=db
            )
            
            if updated is None:
                raise HTTPException(404, "Película no encontrada")
            
            # Confirmar transacción
            db.commit()
            db.refresh(updated)
            return updated
            
        except HTTPException:
            raise
        except IntegrityError:
            db.rollback()
            raise HTTPException(400, "Error de integridad al actualizar la película")
        except Exception as e:
            db.rollback()
            raise HTTPException(400, f"No se pudo actualizar la película: {str(e)}")
    
    # DELETE (soft delete, con transacción)
    
    @staticmethod
    def delete_pelicula(id_pelicula: int, db: Session):
        try:
            # Verificar que existe
            PeliculaService.find_pelicula(id_pelicula, db)
            
            # Delegar al repositorio
            result = PeliculaRepository.delete_pelicula(id_pelicula, db)
            
            if result is None:
                raise HTTPException(404, "Película no encontrada")
            
            # Confirmar transacción
            db.commit()
            return {"message": "Película eliminada exitosamente"}
            
        except HTTPException:
            raise
        except Exception as e:
            db.rollback()
            raise HTTPException(400, f"No se pudo eliminar la película: {str(e)}")
    
    # RESTORE (con transacción)
    
    @staticmethod
    def restore_pelicula(id_pelicula: int, db: Session):
        try:
            result = PeliculaRepository.restore_pelicula(id_pelicula, db)
            if result is None:
                raise HTTPException(404, "Película no encontrada o ya está activa")    
            db.commit()
            db.refresh(result)
            return result
        except Exception as e:
            db.rollback()
            raise HTTPException(400, f"No se pudo restaurar la película: {str(e)}")