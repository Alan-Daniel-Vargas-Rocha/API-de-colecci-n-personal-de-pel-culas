from datetime import datetime
from decimal import Decimal
from typing import Optional
from src.dtos.coleccion.coleccion_response import ColeccionResponseDTO

product_data: list[ColeccionResponseDTO] = [
    ColeccionResponseDTO(
        id_usuario = 1,
        coleccion_id = 1,
        nombre='Mi colección',
        coleccion_created_at=datetime.fromisoformat("2026-05-21T18:45:55+00:00"),
        coleccion_update_at=datetime.fromisoformat("2026-05-21T18:45:55+00:00")
    ),
    ColeccionResponseDTO(
        id_usuario = 2,
        coleccion_id =2,
        nombre='Otra colección',
        descripcion='Colección de películas vistas',
        coleccion_created_at=datetime.fromisoformat("2026-05-21T18:45:55+00:00"),
        coleccion_update_at=datetime.fromisoformat("2026-05-21T18:45:55+00:00")
    )
]