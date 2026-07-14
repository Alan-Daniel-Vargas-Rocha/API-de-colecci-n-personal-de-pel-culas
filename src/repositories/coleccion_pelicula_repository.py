from sqlalchemy.orm import Session
from src.models.coleccion_pelicula import ColeccionPelicula

class ColeccionPeliculaRepository:
    
    @staticmethod
    def get_colecciones_peliculas(db: Session):
        colecciones_peliculas = db.query(ColeccionPelicula).all()
        return colecciones_peliculas
    
    @staticmethod
    def find_coleccion_pelicula(coleccion_id: int, pelicula_id: int, db: Session):
        coleccion_pelicula = db.query(ColeccionPelicula).filter(
            ColeccionPelicula.id_coleccion == coleccion_id,
            ColeccionPelicula.pelicula_id == pelicula_id
        ).first()
        return coleccion_pelicula
    
    @staticmethod
    def create_coleccion_pelicula(data: ColeccionPelicula, db: Session):
        db.add(data)
        db.commit()
        db.refresh(data)
        return data
    
    @staticmethod
    def update_coleccion_pelicula(data: ColeccionPelicula, db: Session):
        coleccion_pelicula = ColeccionPeliculaRepository.find_coleccion_pelicula(
            coleccion_id=data.id_coleccion,
            pelicula_id=data.pelicula_id,
            db=db
        )
        
        if coleccion_pelicula is None:
            return None
        
        coleccion_pelicula.fecha_agregado = data.fecha_agregado
        coleccion_pelicula.opinion = data.opinion

        db.commit()
        db.refresh(coleccion_pelicula)
        return coleccion_pelicula
    
    
    @staticmethod
    def delete_coleccion_pelicula(coleccion_id: int, pelicula_id: int, db: Session):
        coleccion_pelicula = ColeccionPeliculaRepository.find_coleccion_pelicula(
            coleccion_id=coleccion_id,
            pelicula_id=pelicula_id,
            db=db
        )
        
        if coleccion_pelicula is None:
            return None
        
        db.delete(coleccion_pelicula)
        db.commit()