-- Eliminamos las tablas antiguas
DROP TABLE IF EXISTS preguntas CASCADE;
DROP TABLE IF EXISTS encuestas CASCADE;
DROP TABLE IF EXISTS categorias CASCADE;
DROP TABLE IF EXISTS usuarios CASCADE;
DROP TABLE IF EXISTS respuestas_e CASCADE;
DROP TABLE IF EXISTS respuestas CASCADE;

-- Creamos la tabla encuestas
CREATE TABLE encuestas(
    codigo VARCHAR(5) NOT NULL PRIMARY KEY,
    nombre VARCHAR(70) NOT NULL,
    descripcion VARCHAR(400) NOT NULL
);

-- Creamos la tabla de categorias
CREATE TABLE categorias(
    codigo VARCHAR(5) NOT NULL PRIMARY KEY,
    nombre VARCHAR(70) NOT NULL,
    encuesta VARCHAR(5) NOT NULL,
    CONSTRAINT fk_cat_encuesta FOREIGN KEY (encuesta) REFERENCES encuestas(codigo) ON DELETE CASCADE
);

-- Creamos la tabla de preguntas
CREATE TABLE preguntas(
    codigo VARCHAR(5) NOT NULL PRIMARY KEY,
    descripcion VARCHAR(200) NOT NULL,
    categoria VARCHAR(5) NOT NULL,
    CONSTRAINT fk_preg_cat FOREIGN KEY (categoria) REFERENCES categorias(codigo) ON DELETE CASCADE
);

-- Creamos la tabla de Usuarios
CREATE TABLE usuarios(
    cedula VARCHAR(8) NOT NULL PRIMARY KEY,
    nombre VARCHAR(30) NOT NULL,
    apellido VARCHAR(30) NOT NULL,
    correo VARCHAR(50) NOT NULL
);

-- Creamos la tabla de las Encuestas Realizadas
CREATE TABLE respuestas_e(
    cod SERIAL NOT NULL PRIMARY KEY,
    fecha DATE NOT NULL,
    encuesta VARCHAR(5) NOT NULL,
    usuario VARCHAR(8) NOT NULL,
    observacion VARCHAR(400),
    CONSTRAINT fk_respe_encuesta FOREIGN KEY (encuesta) REFERENCES encuestas(codigo) ON DELETE CASCADE,
    CONSTRAINT fk_respe_usuario FOREIGN KEY (usuario) REFERENCES usuarios(cedula) ON DELETE CASCADE
);

-- Creamos la tabla de las Respuestas
CREATE TABLE respuestas(
    cod SERIAL NOT NULL PRIMARY KEY,
    p_aceptacion VARCHAR(15) NOT NULL,
    encuesta INTEGER NOT NULL,
    pregunta VARCHAR(5) NOT NULL,
    CONSTRAINT check_p_aceptacion CHECK (p_aceptacion IN ('81% - 100%', '61% - 80%', '41% - 60%', '21% - 40%', '0% - 20%', 'N/C', 'N/A')),
    CONSTRAINT fk_resp_encuesta FOREIGN KEY (encuesta) REFERENCES respuestas_e(cod) ON DELETE CASCADE,
    CONSTRAINT fk_resp_pregunta FOREIGN KEY (pregunta) REFERENCES preguntas(codigo) ON DELETE CASCADE
)