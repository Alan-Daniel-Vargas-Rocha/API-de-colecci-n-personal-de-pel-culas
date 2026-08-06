from sqlalchemy.orm import Session
from src.dtos.usuarios.usuario_create import UsuarioCreateDTO
from src.dtos.usuarios.usuario_update import UsuarioUpdateDTO
from src.models.usuario import Usuario
from datetime import datetime, timezone

class UsuarioRepository:
    
    @staticmethod
    def get_usuarios(db: Session):
        return db.query(Usuario).filter(Usuario.activo == 1).all()
    
    @staticmethod
    def find_usuario(usuario_id: int, db: Session):
        return db.query(Usuario).filter(
            Usuario.id_usuario == usuario_id,
            Usuario.activo == 1
        ).first()
    
    @staticmethod
    def find_usuario_by_email(email: str, db: Session):
        return db.query(Usuario).filter(Usuario.email == email).first()
    
    @staticmethod
    def find_usuario_including_inactive(usuario_id: int, db: Session):
        return db.query(Usuario).filter(Usuario.id_usuario == usuario_id).first()
    
    @staticmethod
    def create_usuario(dto: UsuarioCreateDTO, db: Session):
        data = Usuario(
            nombre=dto.nombre,
            email=dto.email,
            contraseña=dto.contraseña,
            created_at=datetime.now(timezone.utc),
            updated_at=datetime.now(timezone.utc),
            activo=1
        )
        db.add(data)
        db.flush()
        return data
    
    @staticmethod
    def update_usuario(usuario_id: int, dto: UsuarioUpdateDTO, db: Session):
        usuario = UsuarioRepository.find_usuario(usuario_id, db)
        if not usuario:
            return None
        
        if dto.nombre is not None:
            usuario.nombre = dto.nombre
        if dto.email is not None:
            usuario.email = dto.email
        if dto.contraseña is not None:
            usuario.contraseña = dto.contraseña
        
        usuario.updated_at = datetime.now(timezone.utc)
        db.flush()
        return usuario

    
    @staticmethod
    def delete_usuario(usuario_id: int, db: Session):
        usuario = UsuarioRepository.find_usuario(usuario_id, db)
        if not usuario:
            return None
        
        usuario.activo = 0
        usuario.updated_at = datetime.now(timezone.utc)
        db.flush()
        return usuario
    
    @staticmethod
    def restore_usuario(usuario_id: int, db: Session):
        usuario = UsuarioRepository.find_usuario_including_inactive(usuario_id, db)
        if not usuario or usuario.activo == 1:
            return None
        
        usuario.activo = 1
        usuario.updated_at = datetime.now(timezone.utc)
        db.flush()
        return usuario