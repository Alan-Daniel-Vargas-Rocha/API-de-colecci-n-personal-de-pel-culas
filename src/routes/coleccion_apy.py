from fastapi import APIRouter, Depends
from starlette import status
from typing import List
from sqlalchemy.orm import Session

from src.services.coleccion_service import ColeccionService
from src.dtos.coleccion.coleccion_create import ColeccionCreateDTO
from src.dtos.coleccion.coleccion_response import ColeccionResponseDTO
from src.dtos.coleccion.coleccion_update import ColeccionUpdateDTO
from src.config.database import get_db

# Import router
router = APIRouter(
    prefix="/colecciones",
    tags=["Colecciones"],
)

# ============================================
# 1️⃣ GET: Listar todas las colecciones# ============================================
@router.get(
    "/",
    response_model=List[ColeccionResponseDTO],
    status_code=status.HTTP_200_OK
)
def get_colecciones(db: Session = Depends(get_db)):
    return ColeccionService.get_colecciones(db=db)

# ============================================
# 2️⃣ GET: Obtener una colección específica
# ============================================
@router.get(
    "/{id_coleccion}",
    response_model=ColeccionResponseDTO,
    status_code=status.HTTP_200_OK
)
def find_coleccion(id_coleccion: int, db: Session = Depends(get_db)):
    return ColeccionService.find_coleccion(id_coleccion=id_coleccion, db=db)

# ============================================
# 3️⃣ POST: Crear una nueva colección
# ============================================
@router.post(
    "/",
    response_model=ColeccionResponseDTO,
    status_code=status.HTTP_201_CREATED
)
def create_coleccion(data: ColeccionCreateDTO, db: Session = Depends(get_db)):
    return ColeccionService.create_coleccion(dto=data, db=db)

# ============================================
# 4️⃣ PUT: Actualizar una colección
# ============================================
@router.put(
    "/{id_coleccion}",
    response_model=ColeccionResponseDTO,
    status_code=status.HTTP_202_ACCEPTED
)
def update_coleccion(
    id_coleccion: int,
    data: ColeccionUpdateDTO,
    db: Session = Depends(get_db)
):
    return ColeccionService.update_coleccion(
        id_coleccion=id_coleccion,
        dto=data,
        db=db
    )

# ============================================
# 5️⃣ DELETE: Eliminar una colección (soft delete)
# ============================================
@router.delete(
    "/{id_coleccion}",
    status_code=status.HTTP_204_NO_CONTENT
)
def delete_coleccion(id_coleccion: int, db: Session = Depends(get_db)):
    ColeccionService.delete_coleccion(id_coleccion=id_coleccion, db=db)
    return None

