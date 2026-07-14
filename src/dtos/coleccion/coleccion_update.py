from pydantic import BaseModel, Field
from datetime import datetime
from decimal import Decimal
from typing import Optional

# DTO para la actualización de un producto
class ColeccionUpdateDTO(BaseModel):
    nombre: Optional[str] = Field(
        None, min_length=1,
        max_length=32,
        description="Nombre de la colección")

class Config:
        from_attributes = True