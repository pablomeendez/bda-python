DROP TABLE Trabajadores;
DROP TABLE Laboratorio;
DROP TABLE Ubicacion;

CREATE TABLE Ubicacion (
    id INTEGER PRIMARY KEY,
    dirección VARCHAR(50) NOT NULL,
    provincia VARCHAR(50) NOT NULL,
    códigoPostal VARCHAR(5) NOT NULL,
    ciudad VARCHAR(50) NOT NULL
);

CREATE TABLE Laboratorio (
    id INTEGER PRIMARY KEY,
    nombre VARCHAR(50) NOT NULL,
    especialidad VARCHAR(50) NOT NULL,
    telefono VARCHAR(9) NOT NULL,
    capacidad INTEGER NOT NULL CONSTRAINT capacidad_mayor_cero CHECK (capacidad > 0),
    idUbicación INT NOT NULL REFERENCES Ubicacion(id)
);

CREATE TABLE Trabajadores (
    id INTEGER PRIMARY KEY,
    dni VARCHAR(9) UNIQUE NOT NULL,
    nombre VARCHAR(30) NOT NULL,
    apellido1 VARCHAR(30) NOT NULL,
    apellido2 VARCHAR(30),
    fechaNacimiento DATE NOT NULL,
    fechaAlta DATE NOT NULL,
    puesto VARCHAR(30) NOT NULL,
    salario FLOAT NOT NULL CONSTRAINT salario_mayor_cero CHECK (salario > 0),
    bonus FLOAT NOT NULL CONSTRAINT bonus_mayor_cero CHECK (bonus > 0),
    idLaboratorio INT NOT NULL REFERENCES Laboratorio(id)
);


INSERT INTO Ubicacion (id, dirección, provincia, códigoPostal, ciudad) VALUES
(1, 'Calle de la Ciencia', 'Madrid', '28040', 'Madrid'),
(2, 'Calle de la Tecnología', 'Barcelona', '08080', 'Barcelona'),
(3, 'Calle de la Ingeniería', 'Valencia', '46060', 'Valencia');

INSERT INTO Laboratorio (id, nombre, especialidad, telefono, capacidad, idUbicación) VALUES
(1, 'Laboratorio de Física', 'Física', '912345678', 10, 1),
(2, 'Laboratorio de Química', 'Química', '934567890', 15, 2),
(3, 'Laboratorio de Biología', 'Biología', '945678901', 20, 3);

