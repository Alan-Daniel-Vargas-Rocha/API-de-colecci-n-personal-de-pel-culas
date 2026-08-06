from sqlalchemy.orm import Session
from src.dtos.pelicula.pelicula_created import PeliculaCreateDTO
from src.dtos.pelicula.pelicula_update import PeliculaUpdateDTO
from src.models.pelicula import Pelicula
from datetime import datetime, timezone

class PeliculaRepository:
    
    @staticmethod
    def get_peliculas(db: Session):
        return db.query(Pelicula).filter(Pelicula.activo == 1).all()
    
    @staticmethod
    def find_pelicula(id_pelicula: int, db: Session):
        return db.query(Pelicula).filter(
            Pelicula.id_pelicula == id_pelicula,
            Pelicula.activo == 1
        ).first()
    
    @staticmethod
    def find_pelicula_including_inactive(id_pelicula: int, db: Session):
        return db.query(Pelicula).filter(Pelicula.id_pelicula == id_pelicula).first()
    
    @staticmethod
    def create_pelicula(dto: PeliculaCreateDTO, db: Session):
        data = Pelicula(
            titulo=dto.titulo,
            año=dto.año,
            genero=dto.genero,
            pelicula_created_at=datetime.now(timezone.utc),
            pelicula_updated_at=datetime.now(timezone.utc),
            activo=1
        )
        db.add(data)
        db.flush()
        return data
    
    @staticmethod
    def update_pelicula(id_pelicula: int, dto: PeliculaUpdateDTO, db: Session):
        pelicula = PeliculaRepository.find_pelicula(id_pelicula, db)
        if not pelicula:
            return None
        
        if dto.titulo is not None:
            pelicula.titulo = dto.titulo
        if dto.año is not None:
            pelicula.año = dto.año
        if dto.genero is not None:
            pelicula.genero = dto.genero
        
        pelicula.pelicula_updated_at = datetime.now(timezone.utc)
        db.flush()
        return pelicula
    
    @staticmethod
    def delete_pelicula(id_pelicula: int, db: Session):
        pelicula = PeliculaRepository.find_pelicula(id_pelicula, db)
        if not pelicula:
            return None
        
        pelicula.activo = 0
        pelicula.pelicula_updated_at = datetime.now(timezone.utc)
        db.flush()
        return pelicula
    
    @staticmethod
    def restore_pelicula(id_pelicula: int, db: Session):
        pelicula = PeliculaRepository.find_pelicula_including_inactive(id_pelicula, db)
        if not pelicula or pelicula.activo == 1:
            return None
        
        pelicula.activo = 1
        pelicula.pelicula_updated_at = datetime.now(timezone.utc)
        db.flush()
        return pelicula