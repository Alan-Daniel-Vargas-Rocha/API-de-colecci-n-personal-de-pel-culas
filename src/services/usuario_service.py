from fastapi import HTTPException
from sqlalchemy.exc import IntegrityError
from starlette import status
from sqlalchemy.orm import Session
from datetime import datetime, timezone

from src.dtos.usuarios.usuario_update import UsuarioUpdateDTO
from src.dtos.usuarios.usuario_create import UsuarioCreateDTO
from src.repositories.usuario_repositories import UsuarioRepository

class UsuarioService:
    
    # ============================================
    # 1️⃣ LECTURAS (sin transacción)
    # ============================================
    
    @staticmethod
    def get_usuarios(db: Session):
        return UsuarioRepository.get_usuarios(db=db)
    
    @staticmethod
    def find_usuario(usuario_id: int, db: Session):
        usuario = UsuarioRepository.find_usuario(usuario_id, db)
        
        if not usuario:
            raise HTTPException(404, "Usuario no encontrado")
        
        return usuario
    
    # ============================================
    # 2️⃣ CREATE (con transacción)
    # ============================================
    
    @staticmethod
    def create_usuario(dto: UsuarioCreateDTO, db: Session):
        # 1. Validaciones de negocio (pre-transacción)
        
        # ✅ Validar que el email no esté vacío
        if not dto.email or len(dto.email.strip()) == 0:
            raise HTTPException(400, "El email es obligatorio")
        
        # ✅ Validar formato de email (básico)
        if "@" not in dto.email or "." not in dto.email:
            raise HTTPException(400, "El email no tiene un formato válido")
        
        # ✅ Validar que el nombre no esté vacío
        if not dto.nombre or len(dto.nombre.strip()) == 0:
            raise HTTPException(400, "El nombre es obligatorio")
        
        if len(dto.nombre) > 32:
            raise HTTPException(400, "El nombre excede los 32 caracteres")
        
        # ✅ Validar que la contraseña no esté vacía
        if not dto.contraseña or len(dto.contraseña.strip()) == 0:
            raise HTTPException(400, "La contraseña es obligatoria")
        
        if len(dto.contraseña) < 6:
            raise HTTPException(400, "La contraseña debe tener al menos 6 caracteres")
        
        # ✅ Verificar si el email ya existe
        existing_user = UsuarioRepository.find_usuario_by_email(dto.email, db)
        if existing_user:
            raise HTTPException(400, "El email ya está registrado")
        
        # 2. Control de transacción
        try:
            # ✅ Delegar al repositorio
            nuevo = UsuarioRepository.create_usuario(dto, db)
            
            # ✅ Confirmar transacción
            db.commit()
            db.refresh(nuevo)
            return nuevo
            
        except IntegrityError:
            db.rollback()
            raise HTTPException(400, "Error de integridad: el email ya existe o los datos son inválidos")
        except HTTPException:
            raise
        except Exception as e:
            db.rollback()
            raise HTTPException(500, f"Error interno del servidor: {str(e)}")
    
    # ============================================
    # 3️⃣ UPDATE (con transacción)
    # ============================================
    
    @staticmethod
    def update_usuario(usuario_id: int, dto: UsuarioUpdateDTO, db: Session):
        try:
            # Verificar que existe
            usuario = UsuarioService.find_usuario(usuario_id, db)
            
            # Validaciones de negocio
            if dto.nombre is not None:
                if len(dto.nombre.strip()) == 0:
                    raise HTTPException(400, "El nombre no puede estar vacío")
                if len(dto.nombre) > 32:
                    raise HTTPException(400, "El nombre excede los 32 caracteres")
            
            if dto.email is not None:
                if len(dto.email.strip()) == 0:
                    raise HTTPException(400, "El email no puede estar vacío")
                if "@" not in dto.email or "." not in dto.email:
                    raise HTTPException(400, "El email no tiene un formato válido")
                
                # Verificar que el email no esté en uso por otro usuario
                existing = UsuarioRepository.find_usuario_by_email(dto.email, db)
                if existing and existing.id_usuario != usuario_id:
                    raise HTTPException(400, "El email ya está registrado por otro usuario")
            
            if dto.contraseña is not None:
                if len(dto.contraseña.strip()) == 0:
                    raise HTTPException(400, "La contraseña no puede estar vacía")
                if len(dto.contraseña) < 6:
                    raise HTTPException(400, "La contraseña debe tener al menos 6 caracteres")
            
            # Delegar al repositorio
            updated = UsuarioRepository.update_usuario(usuario_id, dto, db)
            
            if updated is None:
                raise HTTPException(404, "Usuario no encontrado")
            
            db.commit()
            db.refresh(updated)
            return updated
        except HTTPException:
            raise
        except IntegrityError:
            db.rollback()
            raise HTTPException(400, "Error de integridad al actualizar el usuario")
        except Exception as e:
            db.rollback()
            raise HTTPException(400, f"No se pudo actualizar: {str(e)}")
    
    # ============================================
    # 4️⃣ DELETE (soft delete, con transacción)
    # ============================================
    
    @staticmethod
    def delete_usuario(usuario_id: int, db: Session):
        try:
            # ✅ Verificar que existe
            UsuarioService.find_usuario(usuario_id, db)
            
            # ✅ Delegar al repositorio
            result = UsuarioRepository.delete_usuario(usuario_id, db)
            
            if result is None:
                raise HTTPException(404, "Usuario no encontrado")
            
            # ✅ Confirmar transacción
            db.commit()
            return {"message": "Usuario eliminado exitosamente"}
            
        except HTTPException:
            raise
        except Exception as e:
            db.rollback()
            raise HTTPException(400, f"No se pudo eliminar el usuario: {str(e)}")
    
    # ============================================
    # 5️⃣ RESTORE (con transacción)
    # ============================================
    
    @staticmethod
    def restore_usuario(usuario_id: int, db: Session):
        try:
            result = UsuarioRepository.restore_usuario(usuario_id, db)
            
            if result is None:
                raise HTTPException(404, "Usuario no encontrado o ya está activo")
            
            db.commit()
            return result
            
        except HTTPException:
            raise
        except Exception as e:
            db.rollback()
            raise HTTPException(400, f"No se pudo restaurar el usuario: {str(e)}")