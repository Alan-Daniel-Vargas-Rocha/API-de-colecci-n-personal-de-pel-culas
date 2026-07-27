"""
DTO para crear un favorito.
"""
from pydantic import BaseModel, Field
from typing import Optional

class FavoritoCreateDTO(BaseModel):
    
    id_usuario: int = Field(
        ..., 
        description="ID del usuario que marca el favorito"
    )
    tipo: str = Field(
        ..., 
        pattern="^(pelicula|serie)$",
        description="Tipo de favorito: 'pelicula' o 'serie'"
    )
    id_item: int = Field(
        ..., 
        description="ID de la película o serie"
    )

    class Config:
        from_attributes = True