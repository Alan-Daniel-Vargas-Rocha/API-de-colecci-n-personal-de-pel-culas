-- ============================================
-- CREAR BASE DE DATOS
-- ============================================
CREATE DATABASE PeliculasCollection;
GO

USE PeliculasCollection;
GO

-- ============================================
-- TABLA: USUARIO
-- ============================================
CREATE TABLE usuario (
    id_usuario INT PRIMARY KEY IDENTITY(1,1) NOT NULL,
    nombre VARCHAR(32) NOT NULL,
    email VARCHAR(30) NOT NULL,
    created_at DATETIME,
    updated_at DATETIME
);
GO

-- ============================================
-- TABLA: COLECCION
-- ============================================
CREATE TABLE coleccion (
    id_coleccion INT PRIMARY KEY IDENTITY(1,1) NOT NULL,
    id_usuario INT NOT NULL,
    nombre VARCHAR(32) NOT NULL,
    activo BIT NOT NULL DEFAULT 1,  -- Soft delete
    coleccion_created_at DATETIME NOT NULL,
    coleccion_update_at DATETIME NOT NULL,
    CONSTRAINT fk_coleccion_usuario FOREIGN KEY (id_usuario) 
        REFERENCES usuario(id_usuario) ON DELETE CASCADE
);
GO

-- ============================================
-- TABLA: PELICULA
-- ============================================
CREATE TABLE pelicula (
    id_pelicula INT PRIMARY KEY IDENTITY(1,1) NOT NULL,
    titulo VARCHAR(32) NOT NULL,
    año INT NULL,
    genero VARCHAR(30) NOT NULL,
    pelicula_created_at DATETIME NOT NULL,
    pelicula_updated_at DATETIME NOT NULL
);
GO

-- ============================================
-- TABLA: COLECCIONPELICULA (Tabla intermedia)
-- ============================================
CREATE TABLE coleccionpelicula (
    id_coleccion_pelicula INT PRIMARY KEY IDENTITY(1,1) NOT NULL,
    pelicula_id INT NOT NULL,
    id_coleccion INT NOT NULL,
    fecha_agregado DATETIME NOT NULL,
    opinion VARCHAR(255) NULL,
    nombre_personalizado VARCHAR(32) NULL,
    calificacion INT NULL,
    coleccion_pelicula_created_at DATETIME NOT NULL,
    coleccion_pelicula_update_at DATETIME NOT NULL,
    CONSTRAINT fk_cp_coleccion FOREIGN KEY (id_coleccion) 
        REFERENCES coleccion(id_coleccion) ON DELETE CASCADE,
    CONSTRAINT fk_cp_pelicula FOREIGN KEY (pelicula_id) 
        REFERENCES pelicula(id_pelicula),
    CONSTRAINT chk_calificacion CHECK (calificacion IS NULL OR (calificacion >= 1 AND calificacion <= 5))
    EXEC sp_rename 'coleccionpelicula.pelicula_id', 'id_pelicula', 'COLUMN';
);
GO

-- ============================================
-- TABLA: SERIES
-- ============================================
CREATE TABLE series (
    id_serie INT PRIMARY KEY IDENTITY(1,1) NOT NULL,
    titulo VARCHAR(32) NOT NULL,
    año_inicio INT NULL,
    año_fin INT NULL,
    genero VARCHAR(30) NOT NULL,
    temporadas INT NULL,
    episodios INT NULL,
    sinopsis VARCHAR(32) NULL,
    estado VARCHAR(20) NULL,  -- 'En emisión', 'Finalizada', 'Cancelada'
    serie_created_at DATETIME NOT NULL,
    serie_updated_at DATETIME NOT NULL
);
GO

-- ============================================
-- TABLA: COLECCIONSERIE (Tabla intermedia)
-- ============================================
CREATE TABLE coleccionserie (
    id_coleccion_serie INT PRIMARY KEY IDENTITY(1,1) NOT NULL,
    id_serie INT NOT NULL,
    id_coleccion INT NOT NULL,
    fecha_agregado DATETIME NOT NULL,
    opinion VARCHAR(255) NULL,
    calificacion INT NULL,
    nombre_personalizado VARCHAR(32) NULL,
    coleccion_serie_created_at DATETIME NOT NULL,
    coleccion_serie_update_at DATETIME NOT NULL,
    CONSTRAINT fk_cs_coleccion FOREIGN KEY (id_coleccion) 
        REFERENCES coleccion(id_coleccion) ON DELETE CASCADE,
    CONSTRAINT fk_cs_serie FOREIGN KEY (id_serie) 
        REFERENCES series(id_serie),
    CONSTRAINT chk_cs_calificacion CHECK (calificacion IS NULL OR (calificacion >= 1 AND calificacion <= 5))
);
GO

-- ============================================
-- TABLA: FAVORITO
-- ============================================
CREATE TABLE favorito (
    id_favorito INT PRIMARY KEY IDENTITY(1,1) NOT NULL,
    id_usuario INT NOT NULL,
    tipo VARCHAR(20) NOT NULL CHECK (tipo IN ('pelicula', 'serie')),
    id_item INT NOT NULL,
    fecha_agregado DATETIME NOT NULL DEFAULT GETDATE(),
    CONSTRAINT fk_favorito_usuario FOREIGN KEY (id_usuario) 
        REFERENCES usuario(id_usuario) ON DELETE CASCADE,
    CONSTRAINT uk_favorito_unico UNIQUE (id_usuario, tipo, id_item)
);
GO

-- ============================================
-- TABLA: AUDITORIA
-- ============================================
CREATE TABLE auditoria (
    id_auditoria INT PRIMARY KEY IDENTITY(1,1) NOT NULL,
    tabla VARCHAR(50) NOT NULL,
    operacion VARCHAR(20) NOT NULL,
    id_registro INT NOT NULL,
    usuario_id INT NULL,
    datos_anteriores NVARCHAR(MAX) NULL,
    datos_nuevos NVARCHAR(MAX) NULL,
    fecha DATETIME NOT NULL DEFAULT GETDATE(),
    CONSTRAINT fk_auditoria_usuario FOREIGN KEY (usuario_id) 
        REFERENCES usuario(id_usuario) ON DELETE SET NULL
);
GO

-- ============================================
-- ÍNDICES PARA RENDIMIENTO
-- ============================================
-- Índices para coleccion
CREATE INDEX idx_coleccion_usuario ON coleccion(id_usuario);

-- Índices para coleccionpelicula
CREATE INDEX idx_coleccionpelicula_coleccion ON coleccionpelicula(id_coleccion);
CREATE INDEX idx_coleccionpelicula_pelicula ON coleccionpelicula(pelicula_id);

-- Índices para pelicula
CREATE INDEX idx_pelicula_titulo ON pelicula(titulo);
CREATE INDEX idx_pelicula_genero ON pelicula(genero);

-- Índices para series
CREATE INDEX idx_serie_titulo ON series(titulo);
CREATE INDEX idx_serie_genero ON series(genero);

-- Índices para coleccionserie
CREATE INDEX idx_coleccionserie_coleccion ON coleccionserie(id_coleccion);
CREATE INDEX idx_coleccionserie_serie ON coleccionserie(id_serie);

-- Índices para favorito
CREATE INDEX idx_favorito_usuario ON favorito(id_usuario);
CREATE INDEX idx_favorito_tipo_item ON favorito(tipo, id_item);

-- Índices para auditoria
CREATE INDEX idx_auditoria_fecha ON auditoria(fecha DESC);
CREATE INDEX idx_auditoria_tabla_registro ON auditoria(tabla, id_registro);
GO

