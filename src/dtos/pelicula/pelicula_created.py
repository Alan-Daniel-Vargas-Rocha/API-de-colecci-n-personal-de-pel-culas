from pydantic import BaseModel, Field
from datetime import datetime
from decimal import Decimal
from typing import Optional

# DTO para crear un producto
class PeliculaCreateDTO(BaseModel):
    titulo: str = Field (..., description= "Titulo de pelicula")
    año: int = Field(..., description="Año de lanzamiento de la película")
    genero: str = Field(..., description="Género de la película")
    # activo: bool = Field(default=True, description="Indica si la película está activa o no")

class Config:
    from_attributes = True
    