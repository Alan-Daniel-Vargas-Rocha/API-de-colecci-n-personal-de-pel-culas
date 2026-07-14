from fastapi import FastAPI
from src.routes import pelicula_apy, coleccion_apy, usuario_apy,coleccion_pelicula_apy
app = FastAPI()  

@app.get("/")
def read_root():
    return {""}

app.include_router(pelicula_apy.router)
app.include_router(coleccion_apy.router)
app.include_router(usuario_apy.router)
app.include_router(coleccion_pelicula_apy.router)