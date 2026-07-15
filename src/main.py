from fastapi import FastAPI
from src.routes import pelicula_apy, coleccion_apy, usuario_apy,coleccion_pelicula_apy
from pathlib import Path

from fastapi import FastAPI
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles
app = FastAPI()  

BASE_DIR = Path(__file__).resolve().parent

app.mount(
    "/static",
    StaticFiles(directory=BASE_DIR / "static"),
    name="static"
)

@app.get("/", include_in_schema=False)
def mostrar_inicio():
    return FileResponse(
        BASE_DIR / "templates" / "index.html"
    )

app.include_router(pelicula_apy.router)
app.include_router(coleccion_apy.router)
app.include_router(usuario_apy.router)
app.include_router(coleccion_pelicula_apy.router)