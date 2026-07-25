from pydantic import BaseModel, Field
from typing import Optional

# DTO para agregar una serie a una colección
class ColeccionSerieCreateDTO(BaseModel):
    opinion: Optional[str] = Field(
        None, max_length=255,
        description="Opinión personal sobre la serie"
    )
    calificacion: Optional[int] = Field(
        None, ge=1, le=5,
        description="Calificación de la serie (1-5)"
    )

    class Config:
        from_attributes = True