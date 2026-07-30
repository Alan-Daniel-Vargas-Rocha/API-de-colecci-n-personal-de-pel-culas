from fastapi import APIRouter, Depends

from starlette import status

from typing import List

from sqlalchemy.orm import Session

from src.dtos.coleccion_pelicula.coleccion_pelicula_response import ColeccionPeliculaResponseDTO
from src.services.coleccion_pelicula_service import ColeccionPeliculaService
from src.dtos.coleccion_pelicula.coleccion_pelicula_create import ColeccionPeliculaCreateDTO
from src.dtos.coleccion_pelicula.coleccion_pelicula_response import ColeccionPeliculaResponseDTO
from src.dtos.coleccion_pelicula.coleccion_pelicula_update import  ColeccionPeliculaUpdateDTO
from src.config.database import get_db
from src.services.coleccion_pelicula_service import ColeccionPeliculaService

# Import router
router = APIRouter(
    prefix = "/coleccion_pelicula",
    tags = ["Coleccion Pelicula"],
    )

# Create CRUD
@router.get(
    "/",
    response_model = List[ColeccionPeliculaResponseDTO],
    status_code = status.HTTP_200_OK
)


@router.get("/", response_model=List[ColeccionPeliculaResponseDTO])
def get_colecciones_peliculas(db: Session = Depends(get_db)):
    return ColeccionPeliculaService.get_colecciones_peliculas(db=db)

@router.get("/{id_coleccion}/{id_pelicula}", response_model = ColeccionPeliculaResponseDTO, status_code = status.HTTP_200_OK)
def find_coleccion_pelicula(id_coleccion: int, id_pelicula: int, db: Session = Depends(get_db)):
    return ColeccionPeliculaService.find_coleccion_pelicula(id_coleccion = id_coleccion, id_pelicula= id_pelicula, db = db)

@router.post("/", response_model = ColeccionPeliculaResponseDTO, status_code = status.HTTP_201_CREATED)
def create_coleccion_pelicula(data: ColeccionPeliculaCreateDTO, db: Session = Depends(get_db)):
    return ColeccionPeliculaService.create_coleccion_pelicula(dto = data, db = db)

@router.put("/{id_coleccion}", response_model = ColeccionPeliculaResponseDTO, status_code = status.HTTP_202_ACCEPTED)
def update_coleccion_pelicula(id_coleccion: int, data: ColeccionPeliculaUpdateDTO, db: Session = Depends(get_db)):
    return ColeccionPeliculaService.update_coleccion_pelicula(id_coleccion = id_coleccion, dto = data, db = db)

@router.delete("/{id_coleccion}", status_code = status.HTTP_204_NO_CONTENT)
def delete_coleccion_pelicula(id_coleccion: int, db: Session = Depends(get_db)):
    ColeccionPeliculaService.delete_coleccion_pelicula(id_coleccion = id_coleccion, db = db)
        

    