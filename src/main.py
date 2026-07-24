from pathlib import Path
from fastapi import FastAPI
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles

from src.routes import (
    pelicula_apy,
    coleccion_apy,
    usuario_apy,
    coleccion_pelicula_apy
)

app = FastAPI()

BASE_DIR = Path(__file__).resolve().parent.parent
FRONTEND_DIR = BASE_DIR / "posts"

# Montar carpetas estáticas
app.mount("/assets", StaticFiles(directory=FRONTEND_DIR / "assets"), name="assets")
app.mount("/components", StaticFiles(directory=FRONTEND_DIR / "components"), name="components")
app.mount("/pages", StaticFiles(directory=FRONTEND_DIR / "pages"), name="pages")
app.mount("/scripts", StaticFiles(directory=FRONTEND_DIR / "scripts"), name="scripts")
app.mount("/styles", StaticFiles(directory=FRONTEND_DIR / "styles"), name="styles")

# Página principal
@app.get("/", include_in_schema=False)
def mostrar_inicio():
    return FileResponse(FRONTEND_DIR / "index.html")

# Rutas de la API
app.include_router(pelicula_apy.router)
app.include_router(coleccion_apy.router)
app.include_router(usuario_apy.router)
app.include_router(coleccion_pelicula_apy.router)