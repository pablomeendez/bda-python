CREATE TABLE Ubicacion (
    id INTEGER PRIMARY KEY,
    dirección VARCHAR(50),
    provincia VARCHAR(50),
    códigoPostal VARCHAR(5),
    ciudad VARCHAR(50)
);

CREATE TABLE Laboratorio (
    id INTEGER PRIMARY KEY,
    nombre VARCHAR(50),
    especialidad VARCHAR(50),
    teléfono VARCHAR(9),
    capacidad INTEGER,
    idUbicación INT NOT NULL REFERENCES Ubicacion(id)
);

CREATE TABLE Trabajadores (
    id INTEGER PRIMARY KEY,
    dni VARCHAR(9) UNIQUE,
    nombre VARCHAR(30),
    apellido1 VARCHAR(30),
    apellido2 VARCHAR(30),
    fechaNacimiento VARCHAR(30),
    fechaAlta VARCHAR(30),
    puesto VARCHAR(30),
    salario FLOAT,
    -->bonus FLOAT,
    idLaboratorio INT NOT NULL REFERENCES Laboratorio(id)
);

