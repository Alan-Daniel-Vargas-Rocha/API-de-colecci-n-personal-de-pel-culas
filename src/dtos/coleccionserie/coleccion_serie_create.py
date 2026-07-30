from pydantic import BaseModel, Field
from typing import Optional

# DTO para agregar una serie a una colección
class ColeccionSerieCreateDTO(BaseModel):
    id_coleccion: int = Field(
        ..., 
        description="ID de la colección donde se agregará la serie"
    )
    id_serie: int = Field(
        ..., 
        description="ID de la serie del catálogo"
    )
    opinion: Optional[str] = Field(
        None, 
        max_length=255,
        description="Opinión personal sobre la serie"
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
        description="Nombre personalizado para la serie en esta colección"
    )

    class Config:
        from_attributes = True