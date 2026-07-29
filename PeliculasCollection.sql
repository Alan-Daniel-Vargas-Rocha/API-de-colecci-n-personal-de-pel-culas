create database PeliculasCollection

-- Crear tabla PeliculasCollection
use PeliculasCollection
go

-- Crear tabla usuario
create table usuario(
	id_usuario int primary key identity (1,1) not null,
	nombre varchar(32) not null,
	email varchar(30) not null,
	created_at datetime,
	updated_at datetime
);
go

-- Crear tabla coleccion
create table coleccion(
	id_coleccion int primary key identity (1,1) not null,
	id_usuario int not null,
	nombre varchar(32) not null,
	coleccion_created_at datetime not null,
	coleccion_update_at datetime not null

	constraint fk_coleccion_usuario foreign key (id_usuario) references usuario(id_usuario) on delete cascade
);
go

-- crear tabla pelicula
create table pelicula(
	id_pelicula int primary key identity (1,1) not null,
	titulo varchar (32) not null,
	año int null,
	genero varchar(30) not null,
	pelicula_created_at datetime not null,
	pelicula_updated_at datetime not null
);

go

--crear tabla coleccionpelicula
create table coleccionpelicula(
	id_coleccion_pelicula int primary key identity (1,1) not null,
	pelicula_id int not null,
	id_coleccion int not null,
	fecha_agregado datetime not null,
	opinion varchar (255) null,
	coleccion_pelicula_created_at datetime not null,
	coleccion_pelicula_update_at datetime not null

ALTER TABLE coleccionpelicula
ADD nombre_personalizado varchar;

ALTER TABLE coleccionpelicula
ADD calificacion INT NULL CHECK (calificacion BETWEEN 1 AND 5);

ALTER TABLE coleccionpelicula
ADD CONSTRAINT chk_calificacion CHECK (calificacion IS NULL OR (calificacion >= 1 AND calificacion <= 5));

	constraint fk_cp_coleccion foreign key (id_coleccion) references coleccion(id_coleccion) 
	on delete cascade, constraint fk_cp_pelicula foreign key (pelicula_id)
	references pelicula (id_pelicula)

);

CREATE TABLE auditoria (
    id_auditoria INT PRIMARY KEY IDENTITY(1,1) NOT NULL,
    tabla VARCHAR(50) NOT NULL,         
    operacion VARCHAR(20) NOT NULL,     
    id_registro INT NOT NULL,            
    usuario_id INT NULL,                
    datos_anteriores NVARCHAR(MAX) NULL, 
    datos_nuevos NVARCHAR(MAX) NULL,    
    fecha DATETIME NOT NULL DEFAULT GETDATE()  

	 CONSTRAINT fk_auditoria_usuario FOREIGN KEY (usuario_id) 
     REFERENCES usuario(id_usuario) ON DELETE SET NULL
);
go

-- Crear tabla series
create table series(
	id_serie int primary key identity (1,1) not null,
	titulo varchar(32) not null,
	año_inicio int null,
	año_fin int null,
	genero varchar(30) not null,
	temporadas int null,
	serie_created_at datetime not null,
	serie_updated_at datetime not null,
	
ALTER TABLE series
ADD temporadas INT;

ALTER TABLE series
ADD sinopsis INT;

ALTER TABLE series
ADD episodios INT;

ALTER TABLE series
ADD estado Varchar; -- 'En emisión', 'Finalizada', 'Cancelada'

);
go

-- Crear tabla coleccionserie (similar a coleccionpelicula)
CREATE TABLE coleccionserie (
    id_coleccion_serie INT PRIMARY KEY IDENTITY(1,1) NOT NULL,
    serie_id INT NOT NULL,
    id_coleccion INT NOT NULL,
    fecha_agregado DATETIME NOT NULL,
    opinion VARCHAR(255) NULL,
    calificacion INT NULL CHECK (calificacion BETWEEN 1 AND 5),
    nombre_personalizado VARCHAR(32) NULL,
    coleccion_serie_created_at DATETIME NOT NULL,
    coleccion_serie_update_at DATETIME NOT NULL,

    CONSTRAINT fk_cs_coleccion FOREIGN KEY (id_coleccion) 
        REFERENCES coleccion(id_coleccion) ON DELETE CASCADE,
    CONSTRAINT fk_cs_serie FOREIGN KEY (serie_id) 
        REFERENCES series(id_serie)
);
GO

CREATE TABLE favorito (
    id_favorito INT PRIMARY KEY IDENTITY(1,1) NOT NULL,
    id_usuario INT NOT NULL,
    tipo VARCHAR(20) NOT NULL CHECK (tipo IN ('pelicula', 'serie')),
    id_item INT NOT NULL, --Peliculas o Series se consigue el ID
    fecha_agregado DATETIME NOT NULL DEFAULT GETDATE(),

    CONSTRAINT fk_favorito_usuario FOREIGN KEY (id_usuario) 
        REFERENCES usuario(id_usuario) ON DELETE CASCADE,

    -- Evita duplicados: un usuario no puede tener la misma película/serie dos veces
    CONSTRAINT uk_favorito_unico UNIQUE (id_usuario, tipo, id_item)
);
GO

-- Índices para rendimiento
CREATE INDEX idx_favorito_usuario ON favorito(id_usuario);
CREATE INDEX idx_favorito_tipo_item ON favorito(tipo, id_item);
GO



-- Índices para rendimiento
CREATE INDEX idx_coleccionserie_coleccion ON coleccionserie(id_coleccion);
CREATE INDEX idx_coleccionserie_serie ON coleccionserie(serie_id);
GO

-- Índices para series
CREATE INDEX idx_serie_titulo ON series(titulo);
CREATE INDEX idx_serie_genero ON series(genero);
CREATE INDEX idx_coleccionserie_serie ON coleccionserie(serie_id);
CREATE INDEX idx_coleccionserie_coleccion ON coleccionserie(id_coleccion);

-- Indice para peliculas
CREATE INDEX idx_coleccion_usuario ON coleccion(id_usuario);
CREATE INDEX idx_coleccionpelicula_coleccion ON coleccionpelicula(id_coleccion);
CREATE INDEX idx_coleccionpelicula_pelicula ON coleccionpelicula(pelicula_id);
CREATE INDEX idx_pelicula_titulo ON pelicula(titulo);
CREATE INDEX idx_pelicula_genero ON pelicula(genero);

-- Índice para auditoría
CREATE INDEX idx_auditoria_fecha ON auditoria(fecha DESC);
CREATE INDEX idx_auditoria_tabla_registro ON auditoria(tabla, id_registro);
GO
