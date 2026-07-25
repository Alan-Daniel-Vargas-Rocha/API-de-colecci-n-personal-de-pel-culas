from datetime import datetime
from typing import Optional
from src.dtos.coleccionserie.coleccion_serie_response import ColeccionSerieResponseDTO

coleccion_serie_data: list[ColeccionSerieResponseDTO] = [
    ColeccionSerieResponseDTO(
        id_coleccion_serie=1,
        serie_id=1,
        id_coleccion=1,
        fecha_agregado=datetime.fromisoformat("2026-05-21T18:45:55+00:00"),
        opinion='Una de las mejores series de todos los tiempos',
        calificacion=5,
        coleccion_serie_created_at=datetime.fromisoformat("2026-05-21T18:45:55+00:00"),
        coleccion_serie_update_at=datetime.fromisoformat("2026-05-21T18:45:55+00:00")
    ),
    ColeccionSerieResponseDTO(
        id_coleccion_serie=2,
        serie_id=2,
        id_coleccion=1,
        fecha_agregado=datetime.fromisoformat("2026-05-21T18:50:55+00:00"),
        opinion='Excelente serie, aunque el final fue controversial',
        calificacion=4,
        coleccion_serie_created_at=datetime.fromisoformat("2026-05-21T18:50:55+00:00"),
        coleccion_serie_update_at=datetime.fromisoformat("2026-05-21T18:50:55+00:00")
    ),
    ColeccionSerieResponseDTO(
        id_coleccion_serie=3,
        serie_id=3,
        id_coleccion=2,
        fecha_agregado=datetime.fromisoformat("2026-05-22T10:15:30+00:00"),
        opinion='Perfecta para reír y relajarse',
        calificacion=5,
        coleccion_serie_created_at=datetime.fromisoformat("2026-05-22T10:15:30+00:00"),
        coleccion_serie_update_at=datetime.fromisoformat("2026-05-22T10:15:30+00:00")
    ),
    ColeccionSerieResponseDTO(
        id_coleccion_serie=4,
        serie_id=4,
        id_coleccion=2,
        fecha_agregado=datetime.fromisoformat("2026-05-22T11:20:45+00:00"),
        opinion='Muy entretenida, nostalgia de los 80',
        calificacion=4,
        coleccion_serie_created_at=datetime.fromisoformat("2026-05-22T11:20:45+00:00"),
        coleccion_serie_update_at=datetime.fromisoformat("2026-05-22T11:20:45+00:00")
    ),
    ColeccionSerieResponseDTO(
        id_coleccion_serie=5,
        serie_id=5,
        id_coleccion=3,
        fecha_agregado=datetime.fromisoformat("2026-05-22T14:30:10+00:00"),
        opinion='Excelente representación histórica',
        calificacion=5,
        coleccion_serie_created_at=datetime.fromisoformat("2026-05-22T14:30:10+00:00"),
        coleccion_serie_update_at=datetime.fromisoformat("2026-05-22T14:30:10+00:00")
    ),
    ColeccionSerieResponseDTO(
        id_coleccion_serie=6,
        serie_id=1,
        id_coleccion=3,
        fecha_agregado=datetime.fromisoformat("2026-05-22T15:45:20+00:00"),
        opinion='Obra maestra del cine y la televisión',
        calificacion=5,
        coleccion_serie_created_at=datetime.fromisoformat("2026-05-22T15:45:20+00:00"),
        coleccion_serie_update_at=datetime.fromisoformat("2026-05-22T15:45:20+00:00")
    )
]