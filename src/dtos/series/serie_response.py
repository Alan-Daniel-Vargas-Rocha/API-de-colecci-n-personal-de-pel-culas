from pydantic import BaseModel, Field
from datetime import datetime
from typing import Optional

# DTO para la respuesta de una serie
class SerieResponseDTO(BaseModel):
    id_serie: int
    titulo: str
    genero: str
    año_inicio: Optional[int] = None
    año_fin: Optional[int] = None
    temporadas: Optional[int] = None
    episodios: Optional[int] = None
    estado: Optional[str] = None
    sinopsis: Optional[str] = None
    serie_created_at: datetime
    serie_updated_at: datetime

    class Config:
        from_attributes = True