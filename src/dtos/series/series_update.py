from pydantic import BaseModel, Field
from typing import Optional

# DTO para la actualización de una serie
class SerieUpdateDTO(BaseModel):
    titulo: Optional[str] = Field(
        None, min_length=1, max_length=32,
        description="Título de la serie"
    )
    año_inicio: Optional[int] = Field(
        None, description="Año de inicio de la serie"
    )
    año_fin: Optional[int] = Field(
        None, description="Año de finalización de la serie"
    )
    genero: Optional[str] = Field(
        None, min_length=1, max_length=30,
        description="Género de la serie"
    )
    temporadas: Optional[int] = Field(
        None, ge=1,
        description="Número de temporadas"
    )

    class Config:
        from_attributes = True