from pydantic import BaseModel, Field, EmailStr
from datetime import datetime

class UsuarioCreateDTO(BaseModel):
    nombre: str = Field(..., min_length=2, max_length=32, description="Nombre del usuario")
    email: EmailStr = Field(..., max_length=30, description="Correo electrónico del usuario")
    contraseña: str = Field(..., max_length=32, description="Contraseña del usuario")
    
    class Config:
        from_attributes = True