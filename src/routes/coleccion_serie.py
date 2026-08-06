from fastapi import APIRouter, Depends
from starlette import status
from typing import List
from sqlalchemy.orm import Session

from src.services.coleccion_serie_service import ColeccionSerieService
from src.dtos.coleccionserie.coleccion_serie_create import ColeccionSerieCreateDTO
from src.dtos.coleccionserie.coleccion_serie_response import ColeccionSerieResponseDTO
from src.dtos.coleccionserie.coleccion_serie_update import ColeccionSerieUpdateDTO
from src.config.database import get_db

router = APIRouter(
    prefix="/coleccion_serie",
    tags=["Colección-Series"],
)

# ============================================
# 1️⃣ GET: Listar TODAS las relaciones (global)
# ============================================
@router.get(
    "/",
    response_model=List[ColeccionSerieResponseDTO],
    status_code=status.HTTP_200_OK
)
def get_all_colecciones_series(db: Session = Depends(get_db)):
    return ColeccionSerieService.get_all_colecciones_series(db=db)

# ============================================
# 2️⃣ GET: Listar relaciones de UNA colección
# ============================================
@router.get(
    "/coleccion/{id_coleccion}/series",
    response_model=List[ColeccionSerieResponseDTO],
    status_code=status.HTTP_200_OK
)
def get_series_from_coleccion(
    id_coleccion: int,
    db: Session = Depends(get_db)
):
    return ColeccionSerieService.get_series_from_coleccion(
        id_coleccion=id_coleccion,
        db=db
    )

# ============================================
# 3️⃣ GET: Obtener una relación específica
# ============================================
@router.get(
    "/{id_coleccion}/{id_serie}",
    response_model=ColeccionSerieResponseDTO,
    status_code=status.HTTP_200_OK
)
def find_coleccion_serie(
    id_coleccion: int,
    id_serie: int,
    db: Session = Depends(get_db)
):
    return ColeccionSerieService.find_coleccion_serie(
        id_coleccion=id_coleccion,
        id_serie=id_serie,
        db=db
    )

# ============================================
# 4️⃣ POST: Crear una nueva relación
# ============================================
@router.post(
    "/coleccion/{id_coleccion}/serie/{id_serie}",
    response_model=ColeccionSerieResponseDTO,
    status_code=status.HTTP_201_CREATED
)
def add_serie_to_coleccion(
    id_coleccion: int,
    id_serie: int,
    data: ColeccionSerieCreateDTO,
    db: Session = Depends(get_db)
):
    return ColeccionSerieService.add_serie_to_coleccion(
        id_coleccion=id_coleccion,
        id_serie=id_serie,
        dto=data,
        db=db
    )

# ============================================
# 5️⃣ PUT: Actualizar una relación
# ============================================
@router.put(
    "/{id_coleccion}/{id_serie}",
    response_model=ColeccionSerieResponseDTO,
    status_code=status.HTTP_202_ACCEPTED
)
def update_serie_in_coleccion(
    id_coleccion: int,
    id_serie: int,
    data: ColeccionSerieUpdateDTO,
    db: Session = Depends(get_db)
):
    return ColeccionSerieService.update_serie_in_coleccion(
        id_coleccion=id_coleccion,
        id_serie=id_serie,
        dto=data,
        db=db
    )

# ============================================
# 6️⃣ DELETE: Eliminar una relación
# ============================================
@router.delete(
    "/{id_coleccion}/{id_serie}",
    status_code=status.HTTP_204_NO_CONTENT
)
def delete_coleccion_serie(
    id_coleccion: int,
    id_serie: int,
    db: Session = Depends(get_db)
):
    ColeccionSerieService.delete_coleccion_serie(
        id_coleccion=id_coleccion,
        id_serie=id_serie,
        db=db
    )
    return None