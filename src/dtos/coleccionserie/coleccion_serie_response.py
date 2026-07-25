from pydantic import BaseModel, Field
from datetime import datetime
from typing import Optional

# DTO para la respuesta de una serie en colección
class ColeccionSerieResponseDTO(BaseModel):
    id_coleccion_serie: int
    serie_id: int
    id_coleccion: int
    fecha_agregado: datetime
    opinion: Optional[str]
    calificacion: Optional[int]
    coleccion_serie_created_at: datetime
    coleccion_serie_update_at: datetime

    class Config:
        from_attributes = True