from pydantic import BaseModel, Field
from datetime import datetime
from decimal import Decimal
from typing import Optional

# DTO para la respuesta de un producto
class ColeccionResponseDTO(BaseModel):
    id_usuario: int 
    id_coleccion: int
    nombre : str
    coleccion_created_at: datetime
    coleccion_update_at: datetime

class Config:
        from_attributes = True