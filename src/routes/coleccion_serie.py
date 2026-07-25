from fastapi import APIRouter, Depends
from starlette import status
from typing import List
from sqlalchemy.orm import Session

from src.services.coleccion_serie_service import ColeccionSerieService
from src.dtos.coleccionserie.coleccion_serie_create import ColeccionSerieCreateDTO
from src.dtos.coleccionserie.coleccion_serie_response import ColeccionSerieResponseDTO
from src.dtos.coleccionserie.coleccion_serie_update import ColeccionSerieUpdateDTO
from src.config.database import get_db

# Import router
router = APIRouter(
    prefix="/colecciones/{id_coleccion}/series",
    tags=["Colección-Series"],
)

# CRUD para relaciones colección-serie
@router.get("/", response_model=List[ColeccionSerieResponseDTO], status_code=status.HTTP_200_OK)
def get_series_from_coleccion(
    id_coleccion: int, 
    db: Session = Depends(get_db)
):
    return ColeccionSerieService.get_series_from_coleccion(
        id_coleccion=id_coleccion, 
        db=db
    )

@router.get("/{id_serie}", response_model=ColeccionSerieResponseDTO, status_code=status.HTTP_200_OK)
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

@router.post("/{id_serie}", response_model=ColeccionSerieResponseDTO, status_code=status.HTTP_201_CREATED)
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

@router.put("/{id_serie}", response_model=ColeccionSerieResponseDTO, status_code=status.HTTP_202_ACCEPTED)
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

@router.delete("/{id_serie}", status_code=status.HTTP_204_NO_CONTENT)
def remove_serie_from_coleccion(
    id_coleccion: int, 
    id_serie: int, 
    db: Session = Depends(get_db)
):
    ColeccionSerieService.remove_serie_from_coleccion(
        id_coleccion=id_coleccion, 
        id_serie=id_serie, 
        db=db
    )