"""
DTO para actualizar una relación colección-película.

Permite al usuario modificar su opinión, calificación y nombre personalizado.
"""
from pydantic import BaseModel, Field
from typing import Optional

class ColeccionPeliculaUpdateDTO(BaseModel):

    
    opinion: Optional[str] = Field(
        None, 
        max_length=255,
        description="Nueva opinión sobre la película"
    )
    calificacion: Optional[int] = Field(
        None, 
        ge=1, 
        le=5,
        description="Nueva calificación de 1 a 5 estrellas"
    )
    nombre_personalizado: Optional[str] = Field(
        None, 
        max_length=32,
        description="Nuevo nombre personalizado para la película"
    )

    class Config:
        from_attributes = True