from pydantic import BaseModel, Field, EmailStr
from typing import Optional

class UsuarioUpdateDTO(BaseModel):
    nombre: Optional[str] = Field(None, min_length=2, max_length=32, description="Nombre del usuario")
    email: Optional[EmailStr] = Field(None, max_length=30, description="Correo electrónico del usuario")
    
    class Config:
        from_attributes = True