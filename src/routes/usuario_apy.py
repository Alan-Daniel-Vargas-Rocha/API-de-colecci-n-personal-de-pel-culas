from fastapi import APIRouter, Depends
from starlette import status
from typing import List
from sqlalchemy.orm import Session

from src.dtos.usuarios.usuario_response import UsuarioResponseDTO
from src.dtos.usuarios.usuario_create import UsuarioCreateDTO
from src.dtos.usuarios.usuario_update import UsuarioUpdateDTO
from src.services.usuario_service import UsuarioService
from src.config.database import get_db

router = APIRouter(
    prefix="/usuario",
    tags=["Usuarios"]
)

@router.get("/", response_model=List[UsuarioResponseDTO], status_code=status.HTTP_200_OK)
def get_usuarios(db: Session = Depends(get_db)):
    return UsuarioService.get_usuarios(db=db)

@router.get("/{usuario_id}", response_model=UsuarioResponseDTO, status_code=status.HTTP_200_OK)
def find_usuario(usuario_id: int, db: Session = Depends(get_db)):
    return UsuarioService.find_usuario(usuario_id=usuario_id, db=db)

@router.post("/", response_model=UsuarioResponseDTO, status_code=status.HTTP_201_CREATED)
def create_usuario(data: UsuarioCreateDTO, db: Session = Depends(get_db)):
    return UsuarioService.create_usuario(dto=data, db=db)

@router.put("/{usuario_id}", response_model=UsuarioResponseDTO, status_code=status.HTTP_200_OK)
def update_usuario(usuario_id: int, data: UsuarioUpdateDTO, db: Session = Depends(get_db)):
    return UsuarioService.update_usuario(usuario_id=usuario_id, dto=data, db=db)

@router.delete("/{usuario_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_usuario(usuario_id: int, db: Session = Depends(get_db)):
    return UsuarioService.delete_usuario(usuario_id=usuario_id, db=db)