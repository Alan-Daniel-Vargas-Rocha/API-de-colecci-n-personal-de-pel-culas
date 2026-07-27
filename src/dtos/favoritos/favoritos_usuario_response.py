"""
DTO para mostrar favoritos al usuario final.
Combina datos del favorito con la información de la película/serie.
"""
from pydantic import BaseModel
from datetime import datetime
from typing import Optional

class FavoritoUsuarioResponseDTO(BaseModel):
    id_favorito: int
    tipo: str                     # 'pelicula' o 'serie'
    titulo: str                  
    genero: str                   
    año: Optional[int] = None     # Año de estreno (película)
    año_inicio: Optional[int] = None  # Año de inicio (serie)
    año_fin: Optional[int] = None     # Año de fin (serie)
    imagen: Optional[str] = None      # Para futuro: URL de imagen
    fecha_agregado: datetime
    
    class Config:
        from_attributes = True