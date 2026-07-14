from fastapi import HTTPException
from starlette import status
from sqlalchemy.orm import Session
from datetime import datetime, timezone

from src.dtos.usuarios.usuario_update import UsuarioUpdateDTO
from src.dtos.usuarios.usuario_create import UsuarioCreateDTO
from src.models.usuario import Usuario
from src.repositories.usuario_repositories import UsuarioRepository

class UsuarioService:
    
    @staticmethod
    def get_usuarios(db: Session):
        return UsuarioRepository.get_usuarios(db=db)
    
    @staticmethod
    def find_usuario(usuario_id: int, db: Session):
        usuario = UsuarioRepository.find_usuario(usuario_id=usuario_id, db=db)
        
        if not usuario:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Usuario no encontrado"
            )
        
        return usuario
    
    @staticmethod
    def create_usuario(dto: UsuarioCreateDTO, db: Session):
        # Verificar si el email ya existe
        existing_user = UsuarioRepository.find_usuario_by_email(dto.email, db)
        if existing_user:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="El email ya está registrado"
            )
        
        # Crear el usuario
        data = Usuario(
            nombre=dto.nombre,
            email=dto.email,
          
        )
        
        return UsuarioRepository.create_usuario(data=data, db=db)
    
    @staticmethod
    def update_usuario(usuario_id: int, dto: UsuarioUpdateDTO, db: Session):
        # Verificar que el usuario existe
        usuario = UsuarioService.find_usuario(usuario_id, db)
        
        # Obtener solo los campos que vienen en el DTO
        update_data = dto.dict(exclude_unset=True)
        
        # Si se está actualizando el email, verificar que no esté en uso
        if 'email' in update_data:
            existing_user = UsuarioRepository.find_usuario_by_email(update_data['email'], db)
            if existing_user and existing_user.id_usuario != usuario_id:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="El email ya está registrado por otro usuario"
                )
        
        # Actualizar el usuario
        updated_usuario = UsuarioRepository.update_usuario(usuario_id, update_data, db)
        
        if updated_usuario is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Usuario no encontrado"
            )
        
        return updated_usuario
    
    @staticmethod
    def delete_usuario(usuario_id: int, db: Session):
        usuario = UsuarioService.find_usuario(usuario_id, db)
        
        result = UsuarioRepository.delete_usuario(usuario_id, db)
        
        if result is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Usuario no encontrado"
            )
        
        return {"message": "Usuario eliminado exitosamente"}