from pydantic import BaseModel, Field
from datetime import datetime
from decimal import Decimal
from typing import Optional

# DTO para la respuesta de un producto
class PeliculaResponseDTO(BaseModel):
    id_pelicula: int
    titulo: str
    año: int
    genero: str
    # activo: bool
    pelicula_created_at: datetime
    pelicula_updated_at: datetime

class Config:
        from_attributes = True