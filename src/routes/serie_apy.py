from fastapi import APIRouter, Depends
from starlette import status
from typing import List
from sqlalchemy.orm import Session

from src.services.serie_service import SerieService
from src.dtos.series.series_create import SerieCreateDTO
from src.dtos.series.serie_response import SerieResponseDTO
from src.dtos.series.series_update import SerieUpdateDTO
from src.config.database import get_db

# Import router
router = APIRouter(
    prefix="/series",
    tags=["Series"],
)

# CRUD para Series
@router.get("/", response_model=List[SerieResponseDTO], status_code=status.HTTP_200_OK)
def get_series(db: Session = Depends(get_db)):
    return SerieService.get_series(db=db)

@router.get("/{id_serie}", response_model=SerieResponseDTO, status_code=status.HTTP_200_OK)
def find_serie(id_serie: int, db: Session = Depends(get_db)):
    return SerieService.find_serie(id_serie=id_serie, db=db)

@router.post("/", response_model=SerieResponseDTO, status_code=status.HTTP_201_CREATED)
def create_serie(data: SerieCreateDTO, db: Session = Depends(get_db)):
    return SerieService.create_serie(dto=data, db=db)

@router.put("/{id_serie}", response_model=SerieResponseDTO, status_code=status.HTTP_202_ACCEPTED)
def update_serie(id_serie: int, data: SerieUpdateDTO, db: Session = Depends(get_db)):
    return SerieService.update_serie(id_serie=id_serie, dto=data, db=db)

@router.delete("/{id_serie}", status_code=status.HTTP_204_NO_CONTENT)
def delete_serie(id_serie: int, db: Session = Depends(get_db)):
    SerieService.delete_serie(id_serie=id_serie, db=db)