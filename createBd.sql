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
    dni VARCHAR(9) UNIQUE NOT NULL,
    nombre VARCHAR(30) NOT NULL,
    apellido1 VARCHAR(30) NOT NULL,
    apellido2 VARCHAR(30),
    fechaNacimiento  NOT NULL,
    fechaAlta DATE NOT NULL,
    puesto VARCHAR(30) NOT NULL,
    salario FLOAT NOT NULL CONSTRAINT salario_mayor_cero CHECK (salario > 0),
    bonus FLOAT NOT NULL CONSTRAINT bonus_mayor_cero CHECK (bonus > 0),
    idLaboratorio INT NOT NULL REFERENCES Laboratorio(id)
);


