"""
DTO para la respuesta de una relación colección-película.

Incluye todos los campos de la relación para mostrar al usuario.
"""
from pydantic import BaseModel
from datetime import datetime
from typing import Optional

class ColeccionPeliculaResponseDTO(BaseModel):
  
    
    id_coleccion_pelicula: int
    id_coleccion: int
    id_pelicula: int
    fecha_agregado: datetime
    opinion: Optional[str] = None
    calificacion: Optional[int] = None
    nombre_personalizado: Optional[str] = None
    coleccion_pelicula_created_at: datetime
    coleccion_pelicula_update_at: datetime
    
    class Config:
        from_attributes = True