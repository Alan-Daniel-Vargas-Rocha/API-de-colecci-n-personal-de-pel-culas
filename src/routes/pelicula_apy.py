from fastapi import APIRouter, Depends

from starlette import status

from typing import List

from sqlalchemy.orm import Session

from src.dtos.pelicula.pelicula_response import PeliculaResponseDTO
from src.services.pelicula_service import PeliculaService
from src.dtos.pelicula.pelicula_created import PeliculaCreateDTO
from src.dtos.pelicula.pelicula_response import PeliculaResponseDTO
from src.dtos.pelicula.pelicula_update import PeliculaUpdateDTO
from src.config.database import get_db
from src.services.pelicula_service import PeliculaService

# Import router
router = APIRouter(
    prefix = "/pelicula",
    tags = ["Pelicula"],
    )

@router.get("/", response_model = List[PeliculaResponseDTO], status_code = status.HTTP_200_OK)
def get_peliculas(db: Session = Depends(get_db)):
    return PeliculaService.get_peliculas(db = db)

@router.get("/{id_pelicula}", response_model = PeliculaResponseDTO, status_code = status.HTTP_200_OK)
def find_pelicula(id_pelicula: int, db: Session = Depends(get_db
)):
    return PeliculaService.find_pelicula(id_pelicula = id_pelicula, db = db)

@router.post("/", response_model = PeliculaResponseDTO, status_code = status.HTTP_201_CREATED)
def create_pelicula(data: PeliculaCreateDTO, db: Session = Depends(get_db)):
    return PeliculaService.create_pelicula(dto = data, db = db)

# Agrega esto al final de pelicula_apy.py

@router.put("/{id_pelicula}", response_model=PeliculaResponseDTO, status_code=status.HTTP_200_OK)
def update_pelicula(id_pelicula: int, data: PeliculaUpdateDTO, db: Session = Depends(get_db)):
    return PeliculaService.update_pelicula(id_pelicula=id_pelicula, dto=data, db=db)

