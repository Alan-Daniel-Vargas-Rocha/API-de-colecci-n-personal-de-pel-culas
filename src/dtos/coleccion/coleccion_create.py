from pydantic import BaseModel, Field
from typing import Optional

class ColeccionCreateDTO(BaseModel):
    id_usuario: Optional[int] = Field(None, description="ID del usuario propietario de la colección")
    nombre: str = Field(..., max_length=32, description="Nombre de la colección")
    
    class Config:
        from_attributes = True