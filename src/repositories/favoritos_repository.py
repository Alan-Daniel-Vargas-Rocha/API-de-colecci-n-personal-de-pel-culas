"""
Repositorio para manejar las operaciones CRUD de favoritos.
"""
from sqlalchemy.orm import Session
from src.models.favoritos import Favorito
from src.models.pelicula import Pelicula
from src.models.series import Serie
from src.dtos.favoritos.favoritos_create import FavoritoCreateDTO
from src.dtos.favoritos.favoritos_response import FavoritoResponseDTO
from src.dtos.favoritos.favoritos_usuario_response import FavoritoUsuarioResponseDTO
from datetime import datetime, timezone

class FavoritoRepository:
    
    #  LECTURAS
    
    @staticmethod
    def get_favoritos_usuario(id_usuario: int, db: Session):
        """Obtener todos los favoritos de un usuario."""
        favoritos = db.query(Favorito).filter(
            Favorito.id_usuario == id_usuario
        ).all()
        
        return [
            FavoritoResponseDTO(
                id_favorito=f.id_favorito,
                id_usuario=f.id_usuario,
                tipo=f.tipo,
                id_item=f.id_item,
                fecha_agregado=f.fecha_agregado
            )
            for f in favoritos
        ]
    
    @staticmethod
    def get_favoritos_usuario_amigable(id_usuario: int, db: Session):
        """Obtener favoritos de un usuario con datos de la película/serie."""
        favoritos = db.query(Favorito).filter(
            Favorito.id_usuario == id_usuario
        ).all()
        
        resultado = []
        for fav in favoritos:
            if fav.tipo == "pelicula":
                pelicula = db.query(Pelicula).filter(
                    Pelicula.id_pelicula == fav.id_item
                ).first()
                if pelicula:
                    resultado.append(
                        FavoritoUsuarioResponseDTO(
                            id_favorito=fav.id_favorito,
                            tipo="pelicula",
                            titulo=pelicula.titulo,
                            genero=pelicula.genero,
                            año=pelicula.año,
                            fecha_agregado=fav.fecha_agregado
                        )
                    )
            elif fav.tipo == "serie":
                serie = db.query(Serie).filter(
                    Serie.id_serie == fav.id_item
                ).first()
                if serie:
                    resultado.append(
                        FavoritoUsuarioResponseDTO(
                            id_favorito=fav.id_favorito,
                            tipo="serie",
                            titulo=serie.titulo,
                            genero=serie.genero,
                            año_inicio=serie.año_inicio,
                            año_fin=serie.año_fin,
                            fecha_agregado=fav.fecha_agregado
                        )
                    )
        
        return resultado
    
    @staticmethod
    def find_favorito(id_usuario: int, tipo: str, id_item: int, db: Session):
        """Buscar un favorito específico."""
        favorito = db.query(Favorito).filter(
            Favorito.id_usuario == id_usuario,
            Favorito.tipo == tipo,
            Favorito.id_item == id_item
        ).first()
        
        if not favorito:
            return None
        
        return FavoritoResponseDTO(
            id_favorito=favorito.id_favorito,
            id_usuario=favorito.id_usuario,
            tipo=favorito.tipo,
            id_item=favorito.id_item,
            fecha_agregado=favorito.fecha_agregado
        )
    
    @staticmethod
    def find_favorito_by_id(id_favorito: int, db: Session):
        """Buscar un favorito por ID."""
        return db.query(Favorito).filter(
            Favorito.id_favorito == id_favorito
        ).first()
    
    # CREATE
    
    @staticmethod
    def create_favorito(dto: FavoritoCreateDTO, db: Session):
        """Crear un nuevo favorito."""
        data = Favorito(
            id_usuario=dto.id_usuario,
            tipo=dto.tipo,
            id_item=dto.id_item,
            fecha_agregado=datetime.now(timezone.utc)
        )
        
        db.add(data)
        db.flush()  
        
        return data
    
    #  DELETE
    
    @staticmethod
    def delete_favorito(id_favorito: int, db: Session):
        """Eliminar un favorito por ID."""
        favorito = FavoritoRepository.find_favorito_by_id(id_favorito, db)
        
        if not favorito:
            return None
        
        db.delete(favorito)
        db.flush()  
        return True
    
    @staticmethod
    def delete_favorito_by_item(id_usuario: int, tipo: str, id_item: int, db: Session):
        """Eliminar un favorito por usuario, tipo e item."""
        favorito = FavoritoRepository.find_favorito(id_usuario, tipo, id_item, db)
        
        if not favorito:
            return None
        
        db.delete(favorito)
        db.flush()  
        return True