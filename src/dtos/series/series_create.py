from pydantic import BaseModel, Field
from typing import Optional

# DTO para crear una serie
class SerieCreateDTO(BaseModel):
    # Campos obligatorios
    titulo: str = Field(
        ..., 
        min_length=1, 
        max_length=32, 
        description="Título de la serie"
    )
    genero: str = Field(
        ..., 
        min_length=1, 
        max_length=30, 
        description="Género de la serie (Drama, Comedia, etc.)"
    )
    
    # Campos opcionales
    año_inicio: Optional[int] = Field(
        None, 
        description="Año de inicio de la serie"
    )
    año_fin: Optional[int] = Field(
        None, 
        description="Año de finalización de la serie (NULL si sigue en emisión)"
    )
    temporadas: Optional[int] = Field(
        None, 
        ge=1, 
        description="Número de temporadas"
    )
    episodios: Optional[int] = Field( 
        None, 
        ge=1, 
        description="Número total de episodios"
    )
    estado: Optional[str] = Field(  
        None, 
        max_length=20, 
        description="Estado: 'En emisión', 'Finalizada', 'Cancelada'"
    )
    sinopsis: Optional[str] = Field(  
        None, 
        description="Descripción breve de la serie"
    )
    class Config:
        from_attributes = True