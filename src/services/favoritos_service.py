"""
Servicio para gestionar la lógica de negocio de favoritos.
"""
from fastapi import HTTPException
from sqlalchemy.exc import IntegrityError
from starlette import status
from sqlalchemy.orm import Session

from src.dtos.favoritos.favoritos_create import FavoritoCreateDTO
from src.dtos.favoritos.favoritos_response import FavoritoResponseDTO
from src.dtos.favoritos.favoritos_usuario_response import FavoritoUsuarioResponseDTO
from src.repositories.favoritos_repository import FavoritoRepository
from src.repositories.pelicula_repository import PeliculaRepository
from src.repositories.serie_repository import SerieRepository
from src.services.usuario_service import UsuarioService
from src.utils.logger import setup_logger

logger = setup_logger("favorito_service")

class FavoritoService:
    
    #  LECTURAS 
    
    @staticmethod
    def get_favoritos_usuario(id_usuario: int, db: Session):
        """
        Obtener todos los favoritos de un usuario (formato técnico).
        """
        logger.info(f"Obteniendo favoritos del usuario ID: {id_usuario}")
        
        # Lógica de negocio: Verificar que el usuario existe
        UsuarioService.find_usuario(id_usuario, db)
        
        # Delegar al repositorio
        return FavoritoRepository.get_favoritos_usuario(id_usuario, db)
    
    @staticmethod
    def get_favoritos_usuario_amigable(id_usuario: int, db: Session):
        """
        Obtener favoritos de un usuario en formato amigable para el frontend.
        Incluye los datos de la película/serie.
        """
        logger.info(f"Obteniendo favoritos amigables del usuario ID: {id_usuario}")
        
        # Lógica de negocio: Verificar que el usuario existe
        UsuarioService.find_usuario(id_usuario, db)
        
        # Delegar al repositorio
        return FavoritoRepository.get_favoritos_usuario_amigable(id_usuario, db)
    
    #  CREATE 
    
    @staticmethod
    def add_favorito(dto: FavoritoCreateDTO, db: Session):
        """
        Agregar un favorito.
        """
        logger.info(f"Agregando favorito: usuario={dto.id_usuario}, tipo={dto.tipo}, item={dto.id_item}")
        
        # 1. Validaciones de negocio 
        
        # Verificar que el usuario existe
        UsuarioService.find_usuario(dto.id_usuario, db)
        
        # Validar tipo
        if dto.tipo not in ["pelicula", "serie"]:
            raise HTTPException(400, "Tipo inválido. Debe ser 'pelicula' o 'serie'")
        
        # Verificar que el item existe
        if dto.tipo == "pelicula":
            pelicula = PeliculaRepository.find_pelicula(dto.id_item, db)
            if not pelicula:
                raise HTTPException(404, "Película no encontrada")
        else:  # serie
            serie = SerieRepository.find_serie(dto.id_item, db)
            if not serie:
                raise HTTPException(404, "Serie no encontrada")
        
        # Verificar si ya existe
        existing = FavoritoRepository.find_favorito(
            dto.id_usuario, dto.tipo, dto.id_item, db
        )
        if existing:
            logger.warning(f"El favorito ya existe: usuario={dto.id_usuario}, tipo={dto.tipo}, item={dto.id_item}")
            raise HTTPException(400, "Este item ya está en favoritos")
        
        # 2. Control de transacción
        try:
            # Delegar al repositorio
            nuevo = FavoritoRepository.create_favorito(dto, db)
            
            # Confirmar transacción
            db.commit()
            db.refresh(nuevo)
            
            logger.info(f"Favorito agregado: ID={nuevo.id_favorito}")
            return nuevo
            
        except IntegrityError:
            db.rollback()
            logger.error(f"Error de integridad al agregar favorito: usuario={dto.id_usuario}, tipo={dto.tipo}, item={dto.id_item}")
            raise HTTPException(400, "Error de integridad: el favorito ya existe o los datos son inválidos")
        except HTTPException:
            raise
        except Exception as e:
            db.rollback()
            logger.error(f"Error al agregar favorito: {str(e)}")
            raise HTTPException(500, f"Error interno del servidor: {str(e)}")
    
    #  DELETE 
    
    @staticmethod
    def delete_favorito_by_item(id_usuario: int, tipo: str, id_item: int, db: Session):
        """
        Eliminar un favorito por usuario, tipo e item de manera segura.
        """
        logger.warning(f"Intentando eliminar favorito: usuario={id_usuario}, tipo={tipo}, item={id_item}")
        
        # 1. Validaciones de negocio preventivas
        UsuarioService.find_usuario(id_usuario, db)
        
        if tipo not in ["pelicula", "serie"]:
            raise HTTPException(400, "Tipo inválido. Debe ser 'pelicula' o 'serie'")
            
        # Verificar existencia antes de escribir
        existing = FavoritoRepository.find_favorito(id_usuario, tipo, id_item, db)
        if not existing:
            raise HTTPException(404, "El item especificado no se encuentra en tus favoritos")
        
        # 2. Control de transacción
        try:
            FavoritoRepository.delete_favorito_by_item(id_usuario, tipo, id_item, db)
            db.commit()
            logger.info(f"Favorito eliminado: usuario={id_usuario}, tipo={tipo}, item={id_item}")
            return {"message": "Favorito eliminado exitosamente"}
            
        except Exception as e:
            db.rollback()
            logger.error(f"Error al eliminar favorito: usuario={id_usuario}, {str(e)}")
            raise HTTPException(500, f"Error interno del servidor")
    
    @staticmethod
    def delete_favorito_by_item(id_usuario: int, tipo: str, id_item: int, db: Session):
        """
        Eliminar un favorito por usuario, tipo e item.
        """
        logger.warning(f"Eliminando favorito: usuario={id_usuario}, tipo={tipo}, item={id_item}")
        
        # 1. Validaciones de negocio 
        
        # Verificar que el usuario existe
        UsuarioService.find_usuario(id_usuario, db)
        
        # Validar tipo
        if tipo not in ["pelicula", "serie"]:
            raise HTTPException(400, "Tipo inválido. Debe ser 'pelicula' o 'serie'")
        
        # 2. Control de transacción
        try:
            # Delegar al repositorio
            result = FavoritoRepository.delete_favorito_by_item(id_usuario, tipo, id_item, db)
            
            if result is None:
                raise HTTPException(404, "Favorito no encontrado")
            
            # Confirmar transacción
            db.commit()
            
            logger.info(f"Favorito eliminado: usuario={id_usuario}, tipo={tipo}, item={id_item}")
            return {"message": "Favorito eliminado exitosamente"}
            
        except HTTPException:
            raise
        except Exception as e:
            db.rollback()
            logger.error(f"Error al eliminar favorito: usuario={id_usuario}, tipo={tipo}, item={id_item}: {str(e)}")
            raise HTTPException(500, f"Error interno del servidor: {str(e)}")