from sqlalchemy.orm import Session
from src.models.pelicula import Pelicula

class PeliculaRepository:
    
    @staticmethod
    def get_peliculas(db: Session):
        peliculas = db.query(Pelicula).all()
        return peliculas
    
    @staticmethod
    def find_pelicula(id_pelicula: int, db: Session):
        pelicula = db.query(Pelicula).filter(Pelicula.id_pelicula == id_pelicula).first()
        return pelicula
    
    @staticmethod
    def create_pelicula(data: Pelicula, db: Session):
        db.add(data)
        db.commit()
        db.refresh(data)
        return data
    
    @staticmethod
    def update_pelicula(data: Pelicula, db: Session):
        pelicula = PeliculaRepository.find_pelicula(id_pelicula = data.id, db = db)
        
        if pelicula is None:
            return None
        
        pelicula.titulo = data.titulo
        pelicula.description = data.description
        pelicula.release_date = data.release_date
        pelicula.active = data.active

        db.commit()
        db.refresh(pelicula)
        return pelicula
    
    
    @staticmethod
    def delete_pelicula(id_pelicula: int, db: Session):
        pelicula = PeliculaRepository.find_pelicula(id_pelicula = id_pelicula, db = db)
        
        if pelicula is None:
            return None
        
        db.delete(pelicula)
        db.commit()