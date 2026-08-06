from fastapi import APIRouter, Depends
from starlette import status
from typing import List
from sqlalchemy.orm import Session

from src.dtos.coleccion_pelicula.coleccion_pelicula_response import ColeccionPeliculaResponseDTO
from src.services.coleccion_pelicula_service import ColeccionPeliculaService
from src.dtos.coleccion_pelicula.coleccion_pelicula_create import ColeccionPeliculaCreateDTO
from src.dtos.coleccion_pelicula.coleccion_pelicula_update import ColeccionPeliculaUpdateDTO
from src.config.database import get_db

# Import router
router = APIRouter(
    prefix="/coleccion_pelicula",
    tags=["Coleccion Pelicula"],
)

# ============================================
# 1️⃣ GET: Listar todas las relaciones
# ============================================
@router.get(
    "/",
    response_model=List[ColeccionPeliculaResponseDTO],
    status_code=status.HTTP_200_OK
)
def get_colecciones_peliculas(db: Session = Depends(get_db)):
    """Obtener todas las relaciones colección-película."""
    return ColeccionPeliculaService.get_colecciones_peliculas(db=db)

# ============================================
# 2️⃣ GET: Buscar una relación específica
# ============================================
@router.get(
    "/{id_coleccion}/{id_pelicula}",
    response_model=ColeccionPeliculaResponseDTO,
    status_code=status.HTTP_200_OK
)
def find_coleccion_pelicula(
    id_coleccion: int,
    id_pelicula: int,
    db: Session = Depends(get_db)
):
    """Obtener una relación colección-película específica."""
    return ColeccionPeliculaService.find_coleccion_pelicula(
        id_coleccion=id_coleccion,
        id_pelicula=id_pelicula,
        db=db
    )

# ============================================
# 3️⃣ POST: Agregar película a colección
# ============================================
@router.post(
    "/coleccion/{id_coleccion}/pelicula/{id_pelicula}",
    response_model=ColeccionPeliculaResponseDTO,
    status_code=status.HTTP_201_CREATED
)
def add_pelicula_to_coleccion(
    id_coleccion: int,
    id_pelicula: int,
    data: ColeccionPeliculaCreateDTO,  # ✅ DTO sin IDs
    db: Session = Depends(get_db)
):
    """Agrega una película a una colección específica."""
    return ColeccionPeliculaService.add_pelicula_to_coleccion(
        id_coleccion=id_coleccion,
        id_pelicula=id_pelicula,
        dto=data,
        db=db
    )

# ============================================
# 4️⃣ PUT: Actualizar una relación
# ============================================
@router.put(
    "/{id_coleccion}/{id_pelicula}",
    response_model=ColeccionPeliculaResponseDTO,
    status_code=status.HTTP_202_ACCEPTED
)
def update_coleccion_pelicula(
    id_coleccion: int,
    id_pelicula: int,
    data: ColeccionPeliculaUpdateDTO,
    db: Session = Depends(get_db)
):
    """Actualizar una relación colección-película existente."""
    return ColeccionPeliculaService.update_coleccion_pelicula(
        id_coleccion=id_coleccion,
        id_pelicula=id_pelicula,
        dto=data,
        db=db
    )

# ============================================
# 5️⃣ DELETE: Eliminar una relación
# ============================================
@router.delete(
    "/{id_coleccion}/{id_pelicula}",
    status_code=status.HTTP_204_NO_CONTENT
)
def delete_coleccion_pelicula(
    id_coleccion: int,
    id_pelicula: int,
    db: Session = Depends(get_db)
):
    """Eliminar una relación colección-película."""
    ColeccionPeliculaService.delete_coleccion_pelicula(
        id_coleccion=id_coleccion,
        id_pelicula=id_pelicula,
        db=db
    )