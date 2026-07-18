from pydantic import BaseModel, Field
from datetime import datetime
from decimal import Decimal
from typing import Optional

# DTO para la actualización de un producto
class ColeccionPeliculaCreateDTO(BaseModel):
    
    id_coleccion: int = Field(..., description="ID de la colección")
    pelicula_id: int = Field(..., description="ID de la película")
    calificacion: int = Field(None,ge=1, le=5, description="Calificación de 1 a 5 estrellas")
    opinion: Optional[str] = Field(None, description="Opinión sobre la película en la colección")

    class Config:
        from_attributes = True