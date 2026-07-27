"""
Datos de simulación para favoritos.
"""
from datetime import datetime
from src.dtos.favoritos.favoritos_response import FavoritoResponseDTO

favorito_data: list[FavoritoResponseDTO] = [
    # Usuario 1 - Películas favoritas
    FavoritoResponseDTO(
        id_favorito=1,
        id_usuario=1,
        tipo="pelicula",
        id_item=1,  # Inception
        fecha_agregado=datetime.fromisoformat("2026-05-21T18:45:55+00:00")
    ),
    FavoritoResponseDTO(
        id_favorito=2,
        id_usuario=1,
        tipo="pelicula",
        id_item=2,  # The Dark Knight
        fecha_agregado=datetime.fromisoformat("2026-05-21T19:30:00+00:00")
    ),
    # Usuario 1 - Series favoritas
    FavoritoResponseDTO(
        id_favorito=3,
        id_usuario=1,
        tipo="serie",
        id_item=1,  # Breaking Bad
        fecha_agregado=datetime.fromisoformat("2026-05-22T10:15:00+00:00")
    ),
    # Usuario 2 - Películas favoritas
    FavoritoResponseDTO(
        id_favorito=4,
        id_usuario=2,
        tipo="pelicula",
        id_item=3,  # Interstellar
        fecha_agregado=datetime.fromisoformat("2026-05-22T14:30:00+00:00")
    ),
    # Usuario 2 - Series favoritas
    FavoritoResponseDTO(
        id_favorito=5,
        id_usuario=2,
        tipo="serie",
        id_item=4,  # Stranger Things
        fecha_agregado=datetime.fromisoformat("2026-05-23T09:00:00+00:00")
    )
]