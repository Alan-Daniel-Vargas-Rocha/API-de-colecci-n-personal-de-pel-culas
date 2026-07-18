API de Colección Personal de Películas
Descripción del Proyecto
Esta API REST permite gestionar una colección personal de películas. Los usuarios pueden administrar películas, colecciones y la relación entre ellas, incluyendo la posibilidad de agregar una opinión personal sobre cada película en una colección específica.

Tecnologías Utilizadas
FastAPI: Framework web para construir la API.

SQLAlchemy: ORM para la interacción con la base de datos.

SQL Server: Base de datos relacional.

Pydantic: Para la validación de datos y la definición de esquemas (DTOs).


Estructura del Proyecto (Principales Rutas y Endpoints)
Películas
GET /peliculas/: Obtiene la lista de todas las películas.

GET /peliculas/{id_pelicula}: Obtiene los detalles de una película específica.

POST /peliculas/: Crea una nueva película.

PUT /peliculas/{id_pelicula}: Actualiza los datos de una película existente.

DELETE /peliculas/{id_pelicula}: Elimina una película.

Colecciones
GET /colecciones/: Obtiene la lista de todas las colecciones.

GET /colecciones/{id_coleccion}: Obtiene los detalles de una colección específica.

POST /colecciones/: Crea una nueva colección para un usuario.

PUT /colecciones/{id_coleccion}: Actualiza los datos de una colección existente.

DELETE /colecciones/{id_coleccion}: Elimina una colección.

Relación Colección-Película
POST /coleccion-pelicula/: Agrega una película a una colección, permitiendo añadir una opinión.

DELETE /coleccion-pelicula/{coleccion_id}/{pelicula_id}: Elimina una película de una colección.

GET /coleccion-pelicula/: Obtiene todas las relaciones (colección-película).

PUT /coleccion-pelicula/{coleccion_id}/{pelicula_id}: Actualiza la opinión de una película en una colección.
