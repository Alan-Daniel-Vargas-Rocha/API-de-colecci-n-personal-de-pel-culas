from pydantic import BaseModel, Field
from typing import Optional

class ColeccionPeliculaCreateDTO(BaseModel):

    opinion: Optional[str] = Field(
        None, 
        max_length=255,
        description="Opinión personal sobre la película"
    )
    calificacion: Optional[int] = Field(
        None, 
        ge=1, 
        le=5, 
        description="Calificación de 1 a 5 estrellas"
    )
    nombre_personalizado: Optional[str] = Field(
        None, 
        max_length=32,
        description="Nombre personalizado para la película en esta colección"
    )

    class Config:
        from_attributes = True