from sqlalchemy.orm import Session
from src.models.coleccion_pelicula import ColeccionPelicula
from src.dtos.coleccion_pelicula.coleccion_pelicula_update import ColeccionPeliculaUpdateDTO
from datetime import datetime, timezone
from typing import Optional

class ColeccionPeliculaRepository:
    
    @staticmethod
    def get_all_colecciones_peliculas(db: Session):
        return db.query(ColeccionPelicula).filter(ColeccionPelicula.activo == 1).all()
    
    @staticmethod
    def get_peliculas_from_coleccion(id_coleccion: int, db: Session):
        return db.query(ColeccionPelicula).filter(
            ColeccionPelicula.id_coleccion == id_coleccion,
            ColeccionPelicula.activo == 1
        ).all()
    
    @staticmethod
    def update_coleccion_pelicula(
        id_coleccion: int,
        id_pelicula: int,
        dto: ColeccionPeliculaUpdateDTO,
        db: Session
    ):
        """Actualizar una relación (prepara, no hace commit)"""
        coleccion_pelicula = ColeccionPeliculaRepository.find_coleccion_pelicula(id_coleccion, id_pelicula, db)
        if not coleccion_pelicula:
            return None

        if dto.opinion is not None:
            coleccion_pelicula.opinion = dto.opinion
        if dto.calificacion is not None:
            coleccion_pelicula.calificacion = dto.calificacion
        if dto.nombre_personalizado is not None:
            coleccion_pelicula.nombre_personalizado = dto.nombre_personalizado
        
        coleccion_pelicula.coleccion_pelicula_update_at = datetime.now(timezone.utc)
        db.flush()
        return coleccion_pelicula
    
    @staticmethod
    def find_coleccion_pelicula(id_coleccion: int, id_pelicula: int, db: Session):
        return db.query(ColeccionPelicula).filter(
            ColeccionPelicula.id_coleccion == id_coleccion,
            ColeccionPelicula.id_pelicula == id_pelicula,
            ColeccionPelicula.activo == 1
        ).first()
    
    @staticmethod
    def add_pelicula_to_coleccion(
        id_coleccion: int,
        id_pelicula: int,
        opinion: Optional[str],
        calificacion: Optional[int],
        nombre_personalizado: Optional[str],
        db: Session
    ):
        """Crear relación película-colección"""
        data = ColeccionPelicula(
            id_coleccion=id_coleccion,
            id_pelicula=id_pelicula,
            fecha_agregado=datetime.now(timezone.utc),
            opinion=opinion,
            calificacion=calificacion,
            nombre_personalizado=nombre_personalizado,
            coleccion_pelicula_created_at=datetime.now(timezone.utc),
            coleccion_pelicula_update_at=datetime.now(timezone.utc),
            activo=1
        )
        db.add(data)
        db.flush()
        return data
    
    @staticmethod
    def delete_coleccion_pelicula(id_coleccion: int, id_pelicula: int, db: Session):
        """Soft delete: marcar como inactiva (prepara, no hace commit)"""
        coleccion_pelicula = ColeccionPeliculaRepository.find_coleccion_pelicula(id_coleccion, id_pelicula, db)
        if not coleccion_pelicula:
            return None
        
        coleccion_pelicula.activo = 0
        coleccion_pelicula.coleccion_pelicula_update_at = datetime.now(timezone.utc)
        db.flush()
        return coleccion_pelicula