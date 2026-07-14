from datetime import datetime
from decimal import Decimal
from typing import Optional
from src.dtos.coleccion.coleccion_response import ColeccionResponseDTO

product_data: list[ColeccionResponseDTO] = [
    ColeccionResponseDTO(
        id_usuario = 1,
        id_coleccion = 1,
        nombre='Mi colección',
        coleccion_created_at=datetime.fromisoformat("2026-05-21T18:45:55+00:00"),
        coleccion_update_at=datetime.fromisoformat("2026-05-21T18:45:55+00:00")
    ),
    ColeccionResponseDTO(
        id_usuario = 2,
        id_coleccion =2,
        nombre='Otra colección',
        coleccion_created_at=datetime.fromisoformat("2026-05-21T18:45:55+00:00"),
        coleccion_update_at=datetime.fromisoformat("2026-05-21T18:45:55+00:00")
    )
]