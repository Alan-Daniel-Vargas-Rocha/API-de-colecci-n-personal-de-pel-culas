from pydantic import BaseModel, Field
from typing import Optional

# DTO para la actualización de una serie
class SerieUpdateDTO(BaseModel):
    titulo: Optional[str] = Field(
        None, 
        min_length=1, 
        max_length=32,
        description="Nuevo título de la serie"
    )
    genero: Optional[str] = Field(
        None, 
        min_length=1, 
        max_length=30,
        description="Nuevo género de la serie"
    )
    año_inicio: Optional[int] = Field(
        None,
        description="Nuevo año de estreno"
    )
    año_fin: Optional[int] = Field(
        None,
        description="Nuevo año de finalización"
    )
    temporadas: Optional[int] = Field(
        None, 
        ge=1,
        description="Nuevo número de temporadas"
    )
    episodios: Optional[int] = Field(
        None, 
        ge=1,
        description="Nuevo número de episodios"
    )
    estado: Optional[str] = Field(
        None, 
        max_length=20,
        description="Nuevo estado: 'En emisión', 'Finalizada', 'Cancelada'"
    )
    sinopsis: Optional[str] = Field(
        None,
        description="Nueva descripción breve"
    ) 
    titulo: Optional[str] = Field(
        None, 
        min_length=1, 
        max_length=32,
        description="Nuevo título de la serie"
    )
    genero: Optional[str] = Field(
        None, 
        min_length=1, 
        max_length=30,
        description="Nuevo género de la serie"
    )
    año_inicio: Optional[int] = Field(
        None,
        description="Nuevo año de estreno"
    )
    año_fin: Optional[int] = Field(
        None,
        description="Nuevo año de finalización"
    )
    temporadas: Optional[int] = Field(
        None, 
        ge=1,
        description="Nuevo número de temporadas"
    )
    episodios: Optional[int] = Field(
        None, 
        ge=1,
        description="Nuevo número de episodios"
    )
    estado: Optional[str] = Field(
        None, 
        max_length=20,
        description="Nuevo estado: 'En emisión', 'Finalizada', 'Cancelada'"
    )
    sinopsis: Optional[str] = Field(
        None,
        description="Nueva descripción breve"
    )

    class Config:
        from_attributes = True