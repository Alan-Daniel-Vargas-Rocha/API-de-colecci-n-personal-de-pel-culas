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
    coleccion_serie
)

app = FastAPI()

BASE_DIR = Path(__file__).resolve().parent.parent
FRONTEND_DIR = BASE_DIR / "Post"

app.mount("/static", StaticFiles(directory=FRONTEND_DIR / "static"), name="static")

@app.get("/", include_in_schema=False)
def mostrar_inicio():
    return FileResponse(FRONTEND_DIR / "templates" / "index.html")

app.include_router(pelicula_apy.router)
app.include_router(coleccion_apy.router)
app.include_router(usuario_apy.router)
app.include_router(coleccion_pelicula_apy.router)
app.include_router(serie_apy.router)
app.include_router(coleccion_serie.router)