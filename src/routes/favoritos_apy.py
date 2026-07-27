"""
Rutas (endpoints) para gestionar favoritos.

Endpoints disponibles:
- GET /favoritos/usuario/{id_usuario} - Listar favoritos de un usuario
- GET /favoritos/usuario/{id_usuario}/amigable - Listar favoritos con detalles
- POST /favoritos - Agregar favorito
- DELETE /favoritos/{id_favorito} - Eliminar favorito por ID
- DELETE /favoritos/usuario/{id_usuario}/{tipo}/{id_item} - Eliminar favorito por item
"""
from fastapi import APIRouter, Depends, HTTPException
from starlette import status
from typing import List
from sqlalchemy.orm import Session

from src.dtos.favoritos.favoritos_create import FavoritoCreateDTO
from src.dtos.favoritos.favoritos_response import FavoritoResponseDTO
from src.dtos.favoritos.favoritos_usuario_response import FavoritoUsuarioResponseDTO
from src.services.favoritos_service import FavoritoService
from src.config.database import get_db
from src.utils.logger import setup_logger

logger = setup_logger("favorito_api")

router = APIRouter(
    prefix="/favoritos",
    tags=["Favoritos"],
)

# ==================== ENDPOINTS ====================

@router.get(
    "/usuario/{id_usuario}",
    response_model=List[FavoritoResponseDTO],
    status_code=status.HTTP_200_OK,
    summary="Listar favoritos de un usuario",
    description="Obtiene todos los favoritos de un usuario específico."
)
def get_favoritos_usuario(
    id_usuario: int,
    db: Session = Depends(get_db)
):
    """Obtener favoritos de un usuario (formato técnico)."""
    logger.info(f"GET /favoritos/usuario/{id_usuario}")
    return FavoritoService.get_favoritos_usuario(id_usuario, db)



@router.get(
    "/usuario/{id_usuario}",
    response_model=List[FavoritoUsuarioResponseDTO],
    status_code=status.HTTP_200_OK,
    summary="Listar favoritos de un usuario con detalles",
    description="Obtiene los favoritos de un usuario con información completa de la película/serie."
)
def get_favoritos_usuario_amigable(
    id_usuario: int,
    db: Session = Depends(get_db)
):
    """Obtener favoritos de un usuario en formato amigable para el frontend."""
    logger.info(f"GET /favoritos/usuario/{id_usuario}")
    return FavoritoService.get_favoritos_usuario_amigable(id_usuario, db)


@router.post(
    "/",
    response_model=FavoritoResponseDTO,
    status_code=status.HTTP_201_CREATED,
    summary="Agregar favorito",
    description="Agrega una película o serie a favoritos de un usuario."
)
def add_favorito(
    data: FavoritoCreateDTO,
    db: Session = Depends(get_db)
):
    """Agregar un favorito."""
    logger.info(f"POST /favoritos - Agregando favorito: usuario={data.id_usuario}, tipo={data.tipo}")
    return FavoritoService.add_favorito(data, db)


@router.delete(
    "/{id_favorito}",
    status_code=status.HTTP_204_NO_CONTENT,
    summary="Eliminar favorito por ID",
    description="Elimina un favorito por su ID."
)
def delete_favorito(
    id_favorito: int,
    db: Session = Depends(get_db)
):
    """Eliminar un favorito por ID."""
    logger.warning(f"DELETE /favoritos/{id_favorito}")
    FavoritoService.delete_favorito(id_favorito, db)
    return None


@router.delete(
    "/usuario/{id_usuario}/{tipo}/{id_item}",
    status_code=status.HTTP_204_NO_CONTENT,
    summary="Eliminar favorito por item",
    description="Elimina un favorito específico de un usuario."
)
def delete_favorito_by_item(
    id_usuario: int,
    tipo: str,
    id_item: int,
    db: Session = Depends(get_db)
):
    """Eliminar un favorito por usuario, tipo e item."""
    logger.warning(f"DELETE /favoritos/usuario/{id_usuario}/{tipo}/{id_item}")
    
    if tipo not in ["pelicula", "serie"]:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Tipo inválido. Debe ser 'pelicula' o 'serie'"
        )
    
    FavoritoService.delete_favorito_by_item(id_usuario, tipo, id_item, db)
    return None