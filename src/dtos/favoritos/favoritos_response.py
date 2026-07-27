"""
DTO para la respuesta de un favorito.
"""
from pydantic import BaseModel
from datetime import datetime
from typing import Optional

class FavoritoResponseDTO(BaseModel):
    """
    Respuesta completa de un favorito.
    """
    
    id_favorito: int
    id_usuario: int
    tipo: str
    id_item: int
    fecha_agregado: datetime
    
    class Config:
        from_attributes = True