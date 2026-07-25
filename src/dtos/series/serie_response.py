from pydantic import BaseModel, Field
from datetime import datetime
from typing import Optional

# DTO para la respuesta de una serie
class SerieResponseDTO(BaseModel):
    id_serie: int
    titulo: str
    año_inicio: Optional[int]
    año_fin: Optional[int]
    genero: str
    temporadas: Optional[int]
    serie_created_at: datetime
    serie_updated_at: datetime

    class Config:
        from_attributes = True