"""
Servicio para gestionar la lógica de negocio de favoritos.
"""
from fastapi import HTTPException
from starlette import status
from sqlalchemy.orm import Session

from src.dtos.favoritos.favoritos_create import FavoritoCreateDTO
from src.dtos.favoritos.favoritos_response import FavoritoResponseDTO
from src.dtos.favoritos.favoritos_usuario_response import FavoritoUsuarioResponseDTO
from src.models.favoritos import Favorito
from src.models.pelicula import Pelicula
from src.models.series import Serie
from src.repositories.favoritos_repository import FavoritoRepository
from src.services.usuario_service import UsuarioService
from src.utils.logger import setup_logger

logger = setup_logger("favorito_service")

class FavoritoService:
    
    @staticmethod
    def get_favoritos_usuario(id_usuario: int, db: Session):
        """
        Obtener todos los favoritos de un usuario (formato técnico).
        """
        logger.info(f"Obteniendo favoritos del usuario ID: {id_usuario}")
        
        # Verificar que el usuario existe
        UsuarioService.find_usuario(id_usuario, db)
        
        return FavoritoRepository.get_favoritos_usuario(id_usuario, db)
    
    @staticmethod
    def get_favoritos_usuario_amigable(id_usuario: int, db: Session):
        """
        Obtener favoritos de un usuario en formato amigable para el frontend.
        Incluye los datos de la película/serie.
        """
        logger.info(f"Obteniendo favoritos amigables del usuario ID: {id_usuario}")
        
        # Verificar que el usuario existe
        UsuarioService.find_usuario(id_usuario, db)
        
        # Obtener todos los favoritos
        favoritos = FavoritoRepository.get_favoritos_usuario(id_usuario, db)
        
        resultado = []
        for fav in favoritos:
            if fav.tipo == "pelicula":
                item = db.query(Pelicula).filter(Pelicula.id_pelicula == fav.id_item).first()
                if item:
                    resultado.append(
                        FavoritoUsuarioResponseDTO(
                            id_favorito=fav.id_favorito,
                            tipo="pelicula",
                            titulo=item.titulo,
                            genero=item.genero,
                            año=item.año,
                            fecha_agregado=fav.fecha_agregado
                        )
                    )
            elif fav.tipo == "serie":
                item = db.query(Serie).filter(Serie.id_serie == fav.id_item).first()
                if item:
                    resultado.append(
                        FavoritoUsuarioResponseDTO(
                            id_favorito=fav.id_favorito,
                            tipo="serie",
                            titulo=item.titulo,
                            genero=item.genero,
                            año_inicio=item.año_inicio,
                            año_fin=item.año_fin,
                            fecha_agregado=fav.fecha_agregado
                        )
                    )
        
        logger.info(f"Se encontraron {len(resultado)} favoritos")
        return resultado
    
    @staticmethod
    def add_favorito(dto: FavoritoCreateDTO, db: Session):
        """
        Agregar un favorito.
        """
        logger.info(f"Agregando favorito: usuario={dto.id_usuario}, tipo={dto.tipo}, item={dto.id_item}")
        
        # Verificar que el usuario existe
        UsuarioService.find_usuario(dto.id_usuario, db)
        
        # Verificar que el item existe (película o serie)
        if dto.tipo == "pelicula":
            item = db.query(Pelicula).filter(Pelicula.id_pelicula == dto.id_item).first()
            if not item:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail="Película no encontrada"
                )
        elif dto.tipo == "serie":
            item = db.query(Serie).filter(Serie.id_serie == dto.id_item).first()
            if not item:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail="Serie no encontrada"
                )
        else:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Tipo inválido. Debe ser 'pelicula' o 'serie'"
            )
        
        # Verificar si ya existe
        existing = FavoritoRepository.find_favorito(dto.id_usuario, dto.tipo, dto.id_item, db)
        if existing:
            logger.warning(f"El favorito ya existe: usuario={dto.id_usuario}, tipo={dto.tipo}, item={dto.id_item}")
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Este item ya está en favoritos"
            )
        
        # Crear el favorito
        data = Favorito(
            id_usuario=dto.id_usuario,
            tipo=dto.tipo,
            id_item=dto.id_item
        )
        
        result = FavoritoRepository.create_favorito(data, db)
        logger.info(f"Favorito agregado: ID={result.id_favorito}")
        return result
    
    @staticmethod
    def delete_favorito(id_favorito: int, db: Session):
        """
        Eliminar un favorito por su ID.
        """
        logger.warning(f"Eliminando favorito ID: {id_favorito}")
        
        result = FavoritoRepository.delete_favorito(id_favorito, db)
        
        if result is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Favorito no encontrado"
            )
        
        return {"message": "Favorito eliminado exitosamente"}
    
    @staticmethod
    def delete_favorito_by_item(id_usuario: int, tipo: str, id_item: int, db: Session):
        """
        Eliminar un favorito por usuario, tipo e item.
        """
        logger.warning(f"Eliminando favorito: usuario={id_usuario}, tipo={tipo}, item={id_item}")
        
        # Verificar que el usuario existe
        UsuarioService.find_usuario(id_usuario, db)
        
        result = FavoritoRepository.delete_favorito_by_item(id_usuario, tipo, id_item, db)
        
        if result is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Favorito no encontrado"
            )
        
        return {"message": "Favorito eliminado exitosamente"}