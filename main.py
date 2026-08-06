from pathlib import Path
from fastapi import FastAPI
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles

from src.routes import (
    pelicula_apy,
    coleccion_apy,
    usuario_apy,
    coleccion_pelicula_apy,
    serie_apy,
    coleccion_serie,
    favoritos_apy
)

app = FastAPI(
    title= "Sistema de catalogo de colecciones de peliculas y series",
    description= "Esto es un sistema para que el usuario pueda guardar peliculas a su gusto",
    version= "1.0.0"
)
    

@app.get("/")
def read_root():
    return { "message": "Bienvenido al Sistema de Catálogo de Colecciones",
        "version": "1.0.0",
        "documentacion": {
            "swagger": "/docs",
            "redoc": "/redoc"
        },
        "endpoints": {
            "peliculas": "/peliculas",
            "series": "/series",
            "colecciones": "/colecciones",
            "coleccion_pelicula": "/coleccion_pelicula",
            "coleccion_serie": "/coleccion_serie",
            "usuarios": "/usuarios",
            "favoritos": "/favoritos"
            }
    }

app.include_router(pelicula_apy.router)
app.include_router(coleccion_apy.router)
app.include_router(usuario_apy.router)
app.include_router(coleccion_pelicula_apy.router)
app.include_router(serie_apy.router)
app.include_router(coleccion_serie.router)
app.include_router(favoritos_apy.router)