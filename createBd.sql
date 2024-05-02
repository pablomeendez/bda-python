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
    DNI VARCHAR(9) UNIQUE,
    nombre VARCHAR(50),
    apellido1 VARCHAR(50),
    apellido2 VARCHAR(50),
    fechaNacimiento DATE,
    fechaAlta DATE,
    puesto VARCHAR(50),
    salario FLOAT,
    -->bonus FLOAT,
    idLaboratorio INT NOT NULL REFERENCES Laboratorio(id)
);

