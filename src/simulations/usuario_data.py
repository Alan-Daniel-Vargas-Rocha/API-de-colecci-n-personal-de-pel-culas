from datetime import datetime
from decimal import Decimal
from typing import Optional
from src.dtos.usuarios.usuario_response import UsuarioResponseDTO

product_data: list[UsuarioResponseDTO] = [
    UsuarioResponseDTO(
        id_usuario = 1,
        nombre = 'Roberto',
        email = 'usuario1@gmail.com',
        created_at=datetime.fromisoformat("2026-05-21T18:45:55+00:00"),
        updated_at=datetime.fromisoformat("2026-05-21T18:45:55+00:00")
    ),
    UsuarioResponseDTO(
        id_usuario=2,
        nombre='Carlos',
        email = 'usuario2@gmail.com',
        created_at=datetime.fromisoformat("2026-05-21T18:45:55+00:00"),
        updated_at=datetime.fromisoformat("2026-05-21T18:45:55+00:00")
    )
]
