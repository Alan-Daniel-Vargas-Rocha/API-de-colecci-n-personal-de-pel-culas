from pydantic import BaseModel, Field
from datetime import datetime
from decimal import Decimal
from typing import Optional

# DTO para crear un producto
class ColeccionCreateDTO(BaseModel):
    id_usuario: int = Field(..., description="ID del usuario propietario")
    nombre: str = Field(..., description="Nombre de la colección")
   

    class Config:
        from_attributes = True