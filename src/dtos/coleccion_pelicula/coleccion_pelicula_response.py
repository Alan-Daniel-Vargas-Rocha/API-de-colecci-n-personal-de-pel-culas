from pydantic import BaseModel, Field
from datetime import datetime
from decimal import Decimal
from typing import Optional

# DTO para la respuesta de un producto
class ColeccionPeliculaResponseDTO(BaseModel):
    id_coleccion: int
    pelicula_id: int
    fecha_agregado: datetime
    opinion: Optional[str] = None
    calificacion: Optional[int] = None
    coleccion_pelicula_created_at: datetime
    coleccion_pelicula_update_at: datetime
    
     
class Config:
    from_attributes = True