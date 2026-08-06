from sqlalchemy.orm import Session
from src.models.favoritos import Favorito
from src.models.pelicula import Pelicula
from src.models.series import Serie
from src.dtos.favoritos.favoritos_create import FavoritoCreateDTO
from src.dtos.favoritos.favoritos_usuario_response import FavoritoUsuarioResponseDTO
from datetime import datetime, timezone

class FavoritoRepository:
    
    #  LECTURAS (Retornando siempre Modelos)
    
    @staticmethod
    def get_favoritos_usuario(id_usuario: int, db: Session):
        """Obtener todos los favoritos de un usuario como entidades puras."""
        return db.query(Favorito).filter(Favorito.id_usuario == id_usuario).all()
    
    @staticmethod
    def get_favoritos_usuario_amigable(id_usuario: int, db: Session):
        """Obtener favoritos optimizados en rendimiento (Máximo 3 consultas)."""
        favoritos = db.query(Favorito).filter(Favorito.id_usuario == id_usuario).all()
        if not favoritos:
            return []
            
        # Agrupamos IDs por tipo para hacer búsquedas masivas con IN
        id_peliculas = [f.id_item for f in favoritos if f.tipo == "pelicula"]
        id_series = [f.id_item for f in favoritos if f.tipo == "serie"]
        
        # Consultas masivas eficientes
        peliculas_dict = {p.id_pelicula: p for p in db.query(Pelicula).filter(Pelicula.id_pelicula.in_(id_peliculas)).all()} if id_peliculas else {}
        series_dict = {s.id_serie: s for s in db.query(Serie).filter(Serie.id_serie.in_(id_series)).all()} if id_series else {}
        
        resultado = []
        for fav in favoritos:
            if fav.tipo == "pelicula" and fav.id_item in peliculas_dict:
                p = peliculas_dict[fav.id_item]
                resultado.append(FavoritoUsuarioResponseDTO(
                    id_favorito=fav.id_favorito, tipo="pelicula", titulo=p.titulo,
                    genero=p.genero, año=p.año, fecha_agregado=fav.fecha_agregado
                ))
            elif fav.tipo == "serie" and fav.id_item in series_dict:
                s = series_dict[fav.id_item]
                resultado.append(FavoritoUsuarioResponseDTO(
                    id_favorito=fav.id_favorito, tipo="serie", titulo=s.titulo,
                    genero=s.genero, año_inicio=s.año_inicio, año_fin=s.año_fin, fecha_agregado=fav.fecha_agregado
                ))
        return resultado
    
    @staticmethod
    def find_favorito(id_usuario: int, tipo: str, id_item: int, db: Session):
        """Buscar un favorito específico retornando el Modelo para uso seguro del Servicio."""
        return db.query(Favorito).filter(
            Favorito.id_usuario == id_usuario,
            Favorito.tipo == tipo,
            Favorito.id_item == id_item
        ).first()
    
    @staticmethod
    def find_favorito_by_id(id_favorito: int, db: Session):
        """Buscar un favorito por ID."""
        return db.query(Favorito).filter(Favorito.id_favorito == id_favorito).first()
    
    # CREATE (con flush)
    
    @staticmethod
    def create_favorito(dto: FavoritoCreateDTO, db: Session):
        data = Favorito(
            id_usuario=dto.id_usuario,
            tipo=dto.tipo,
            id_item=dto.id_item,
            fecha_agregado=datetime.now(timezone.utc)
        )
        db.add(data)
        db.flush()  
        return data
    
    # DELETE (con flush)
    
    @staticmethod
    def delete_favorito(id_favorito: int, db: Session):
        favorito = FavoritoRepository.find_favorito_by_id(id_favorito, db)
        if not favorito:
            return None
        
        db.delete(favorito)
        db.flush()  
        return favorito
    
    @staticmethod
    def delete_favorito_by_item(id_usuario: int, tipo: str, id_item: int, db: Session):
        favorito = db.query(Favorito).filter(
            Favorito.id_usuario == id_usuario,
            Favorito.tipo == tipo,
            Favorito.id_item == id_item
        ).first()
        
        if not favorito:
            return None
        
        db.delete(favorito)
        db.flush()  
        return favorito
