from pydantic import BaseModel, Field
from datetime import datetime
from decimal import Decimal
from typing import Optional

# DTO para la actualización de un producto
class PeliculaUpdateDTO(BaseModel):
    titulo: Optional[str] = Field(min_length=2, max_length=100)
    año: Optional[int] = Field(gt=1800, lt=datetime.now().year + 1)
    genero: Optional[str] = Field(max_length=50)
    # activo: Optional[bool] = None

class Config:
    from_attributes = True
  