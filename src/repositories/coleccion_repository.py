from sqlalchemy.orm import Session
from src.dtos.coleccion.coleccion_create import ColeccionCreateDTO
from src.dtos.coleccion.coleccion_update import ColeccionUpdateDTO
from src.models.coleccion import Coleccion
from datetime import datetime, timezone

class ColeccionRepository:
    
    @staticmethod
    def get_colecciones(db: Session):
        return db.query(Coleccion).filter(Coleccion.activo == 1).all()
    
    @staticmethod
    def find_coleccion(id_coleccion: int, db: Session):
        return db.query(Coleccion).filter(
            Coleccion.id_coleccion == id_coleccion,
            Coleccion.activo == 1
        ).first()
    
    @staticmethod
    def find_coleccion_including_inactive(id_coleccion: int, db: Session):
        return db.query(Coleccion).filter(Coleccion.id_coleccion == id_coleccion).first()
    
    @staticmethod
    def create_coleccion(id_usuario: int, nombre: str, db: Session):
        data = Coleccion(
            id_usuario=id_usuario,
            nombre=nombre,
            coleccion_created_at=datetime.now(timezone.utc),
            coleccion_update_at=datetime.now(timezone.utc),
            activo=1
        )
        db.add(data)
        db.flush()
        return data
    
    @staticmethod
    def update_coleccion(id_coleccion: int, dto: ColeccionUpdateDTO, db: Session):
       
        coleccion = db.get(Coleccion, id_coleccion)
        if not coleccion or coleccion.activo == 0:
            return None
        
        if dto.nombre is not None:
            coleccion.nombre = dto.nombre
        
        coleccion.coleccion_update_at = datetime.now(timezone.utc)
        db.flush()
        return coleccion
    
    @staticmethod
    def delete_coleccion(id_coleccion: int, db: Session):
        coleccion = db.get(Coleccion, id_coleccion)
        if not coleccion or coleccion.activo == 0:
            return None
        
        coleccion.activo = 0
        coleccion.coleccion_update_at = datetime.now(timezone.utc)
        db.flush()
        return coleccion
    
    @staticmethod
    def restore_coleccion(id_coleccion: int, db: Session):
        coleccion = ColeccionRepository.find_coleccion_including_inactive(id_coleccion, db)
        if not coleccion or coleccion.activo == 1:
            return None
        
        coleccion.activo = 1
        coleccion.coleccion_update_at = datetime.now(timezone.utc)
        db.flush()
        return coleccion