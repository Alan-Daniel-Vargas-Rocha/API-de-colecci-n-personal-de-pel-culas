from pydantic import BaseModel, EmailStr
from datetime import datetime
from typing import Optional

class UsuarioResponseDTO(BaseModel):
    id_usuario: int
    nombre: str
    email: str
    contraseña: Optional[str] = None
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None
    
    class Config:
        from_attributes = True