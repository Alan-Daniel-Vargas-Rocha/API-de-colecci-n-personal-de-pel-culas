from decimal import Decimal
from datetime import datetime
from typing import Optional
from src.dtos.coleccion_pelicula.coleccion_pelicula_response import  ColeccionPeliculaResponseDTO

product_data: list[ColeccionPeliculaResponseDTO] = [
    ColeccionPeliculaResponseDTO(
        id_coleccion_pelicula=1,
        id_coleccion=1,
        pelicula_id=1,
        created_at=datetime.fromisoformat("2026-05-21T18:45:55+00:00"),
        updated_at=datetime.fromisoformat("2026-05-21T18:45:55+00:00")
    ),
    ColeccionPeliculaResponseDTO(
        id_coleccion_pelicula=2,
        id_coleccion=1,
        pelicula_id=2,
        created_at=datetime.fromisoformat("2026-05-21T18:45:55+00:00"),
        updated_at=datetime.fromisoformat("2026-05-21T18:45:55+00:00")
    )
   
]
    