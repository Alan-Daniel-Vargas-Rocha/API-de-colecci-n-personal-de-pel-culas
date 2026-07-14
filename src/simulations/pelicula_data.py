from datetime import datetime
from decimal import Decimal
from typing import Optional
from src.dtos.pelicula.pelicula_response import PeliculaResponseDTO

product_data: list[PeliculaResponseDTO] = [
    PeliculaResponseDTO(
        id_pelicula=1,
        titulo='La La Land',
        año=2016,
        genero='Musical',
        # activo=True,
        peliculas_created_at=datetime.fromisoformat("2026-05-21T18:45:55+00:00"),
        updated_at=datetime.fromisoformat("2026-05-21T18:45:55+00:00")
    ),
    PeliculaResponseDTO(
        id_pelicula=2,
        titulo='El Padrino',
        año=1972,
        genero='Drama',
        # activo=True,
        created_at=datetime.fromisoformat("2026-05-21T18:45:55+00:00"),
        updated_at=datetime.fromisoformat("2026-05-21T18:45:55+00:00")
    )
   
]