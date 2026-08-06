from pydantic import BaseModel, Field
from datetime import datetime
from typing import Optional

# DTO para la respuesta de una serie en colección
class ColeccionSerieResponseDTO(BaseModel):
    # Datos de la relación
    id_coleccion_serie: int
    id_coleccion: int
    id_serie: int
    fecha_agregado: datetime
    opinion: Optional[str] = None
    calificacion: Optional[int] = None
    nombre_personalizado: Optional[str] = None
    coleccion_serie_created_at: datetime
    coleccion_serie_update_at: datetime
    activo: int 
    
    # Datos de la serie (del catálogo)
    titulo: Optional[str] = None
    genero: Optional[str] = None
    año_inicio: Optional[int] = None
    año_fin: Optional[int] = None
    temporadas: Optional[int] = None
    episodios: Optional[int] = None
    estado: Optional[str] = None
    sinopsis: Optional[str] = None
    
    class Config:
        from_attributes = True