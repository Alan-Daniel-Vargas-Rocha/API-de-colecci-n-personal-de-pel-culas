from datetime import datetime
from typing import Optional
from src.dtos.series.serie_response import SerieResponseDTO

serie_data: list[SerieResponseDTO] = [
    SerieResponseDTO(
        id_serie=1,
        titulo='Breaking Bad',
        año_inicio=2008,
        año_fin=2013,
        genero='Drama',
        temporadas=5,
        serie_created_at=datetime.fromisoformat("2026-05-21T18:45:55+00:00"),
        serie_updated_at=datetime.fromisoformat("2026-05-21T18:45:55+00:00")
    ),
    SerieResponseDTO(
        id_serie=2,
        titulo='Game of Thrones',
        año_inicio=2011,
        año_fin=2019,
        genero='Fantasía',
        temporadas=8,
        serie_created_at=datetime.fromisoformat("2026-05-21T18:45:55+00:00"),
        serie_updated_at=datetime.fromisoformat("2026-05-21T18:45:55+00:00")
    ),
    SerieResponseDTO(
        id_serie=3,
        titulo='The Office',
        año_inicio=2005,
        año_fin=2013,
        genero='Comedia',
        temporadas=9,
        serie_created_at=datetime.fromisoformat("2026-05-21T18:45:55+00:00"),
        serie_updated_at=datetime.fromisoformat("2026-05-21T18:45:55+00:00")
    ),
    SerieResponseDTO(
        id_serie=4,
        titulo='Stranger Things',
        año_inicio=2016,
        año_fin=None,
        genero='Ciencia Ficción',
        temporadas=4,
        serie_created_at=datetime.fromisoformat("2026-05-21T18:45:55+00:00"),
        serie_updated_at=datetime.fromisoformat("2026-05-21T18:45:55+00:00")
    ),
    SerieResponseDTO(
        id_serie=5,
        titulo='The Crown',
        año_inicio=2016,
        año_fin=2023,
        genero='Drama Histórico',
        temporadas=6,
        serie_created_at=datetime.fromisoformat("2026-05-21T18:45:55+00:00"),
        serie_updated_at=datetime.fromisoformat("2026-05-21T18:45:55+00:00")
    )
]