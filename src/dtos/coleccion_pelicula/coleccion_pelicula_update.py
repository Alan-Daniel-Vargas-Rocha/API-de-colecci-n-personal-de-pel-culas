from pydantic import BaseModel, Field
from datetime import datetime
from decimal import Decimal
from typing import Optional

# DTO para la actualización de un producto
class ColeccionPeliculaUpdateDTO(BaseModel):
  
  
    opinion: Optional[str] = Field(None, description="Opinión sobre la película en la colección")

    class Config:
        from_attributes = True