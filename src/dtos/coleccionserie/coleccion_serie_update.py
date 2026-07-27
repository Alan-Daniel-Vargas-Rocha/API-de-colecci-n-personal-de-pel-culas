from pydantic import BaseModel, Field
from typing import Optional

# DTO para actualizar la relación colección-serie
class ColeccionSerieUpdateDTO(BaseModel):
    opinion: Optional[str] = Field(
        None, 
        max_length=255,
        description="Nueva opinión sobre la serie"
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
        description="Nuevo nombre personalizado para la serie"
    )

    class Config:
        from_attributes = True