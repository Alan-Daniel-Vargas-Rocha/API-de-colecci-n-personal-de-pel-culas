from sqlalchemy.orm import Session
from src.models.usuario import Usuario

class UsuarioRepository:
    
    @staticmethod
    def get_usuarios(db: Session):
        return db.query(Usuario).all()
    
    @staticmethod
    def find_usuario(usuario_id: int, db: Session):
        return db.query(Usuario).filter(Usuario.id_usuario == usuario_id).first()
    
    @staticmethod
    def find_usuario_by_email(email: str, db: Session):
        return db.query(Usuario).filter(Usuario.email == email).first()
    
    @staticmethod
    def create_usuario(data: Usuario, db: Session):
        db.add(data)
        db.commit()
        db.refresh(data)
        return data
    
    @staticmethod
    def update_usuario(usuario_id: int, data: dict, db: Session):
        usuario = UsuarioRepository.find_usuario(usuario_id, db)
        if usuario is None:
            return None
        
        for key, value in data.items():
            if hasattr(usuario, key):
                setattr(usuario, key, value)
        
        db.commit()
        db.refresh(usuario)
        return usuario
    
    @staticmethod
    def delete_usuario(usuario_id: int, db: Session):
        usuario = UsuarioRepository.find_usuario(usuario_id, db)
        if usuario is None:
            return None
        
        db.delete(usuario)
        db.commit()
        return usuario