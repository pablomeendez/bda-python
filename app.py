import psycopg2
import psycopg2.extras
import psycopg2.extensions
import psycopg2.errorcodes

## ------------------------------------------------------------
def connect_db():
    try:   
        conn = psycopg2.connect("")
        conn.autocommit = False
        conn.set_isolation_level(psycopg2.extensions.ISOLATION_LEVEL_SERIALIZABLE)
        print("Nivel de aislamiento: SERIALIZABLE")
        return conn
    except Exception as e:
        print(f"Erro de conexión: {e}")
        sys.exit(1)


## ------------------------------------------------------------
def disconnect_db(conn):
    conn.commit()
    conn.close()


#MOSTRAR SI ES MODO SERIALIZABLE O READCOMMITED
## ------------------------------------------------------------
# ALTA
def add_worker(conn):
    id = input("Id del trabajador: ")
    id = None if id == '' else int(id)
    dni = input("DNI del trabajador: ")
    dni = None if dni == '' else dni
    nombre = input("Nombre del trabajador: ")
    nombre = None if nombre == '' else nombre
    apellido1 = input("Primer apellido: ")
    apellido1 = None if apellido1 == '' else apellido1
    apellido2 = input("Segundo apellido: ")
    apellido2 = None if apellido2 == '' else apellido2
    fechaNacimiento = input("Fecha Nacimiento: ")
    fechaNacimiento = None if fechaNacimiento == '' else fechaNacimiento
    fechaAlta = input("Fecha Alta: ")
    fechaAlta = None if fechaAlta == '' else fechaAlta
    puesto = input("Puesto: ")
    puesto = None if puesto == '' else puesto
    salario = input("Salario: ")
    salario = None if salario == '' else float(salario)
    bonus = input("Bonus: ")
    bonus = None if bonus == '' else float(bonus)
    laboratorio = input("Laboratorio: ")
    laboratorio = None if laboratorio == '' else int(laboratorio)

    sql_query = """insert into Trabajadores(id, dni, nombre, apellido1, apellido2, fechaNacimiento, fechaAlta, puesto, salario, bonus, idLaboratorio) 
                   values(%(id)s, %(dni)s, %(n)s, %(a1)s, %(a2)s, %(fn)s, %(fa)s, %(p)s, %(s)s, %(b)s, %(idl)s)"""
    with conn.cursor() as curr:
        try: 
            curr.execute(sql_query, {'id': id, 'dni': dni, 'n': nombre, 'a1': apellido1, 'a2': apellido2, 'fn': fechaNacimiento, 'fa': fechaAlta, 'p': puesto, 's': salario, 'b': bonus, 'idl': laboratorio})
            conn.commit()
            print("Trabajador añadido")
        except psycopg2.Error as e:
            if e.pgcode == psycopg2.errorcodes.UNIQUE_VIOLATION:
                print("O traballador xa existe")
            elif e.pgcode == psycopg2.errorcodes.NOT_NULL_VIOLATION:
                if e.diag.column_name == 'id':
                    print("Id no puede ser nula.")
                elif e.diag.column_name == 'nombre':
                    print("El nombre no puede ser nulo.")
                elif e.diag.column_name == 'apellido1':
                    print("El primer apellido no puede ser nulo.")
                elif e.diag.column_name == 'puesto':
                    print("El puesto no puede ser nulo.")
                elif e.diag.column_name == 'salario':
                    print("El salario no puede ser nulo.")
                elif e.diag.column_name == 'idLaboratorio':
                    print("El laboratorio no puede ser nulo.")
            elif e.pgcode == psycopg2.errorcodes.FOREIGN_KEY_VIOLATION:
                print("Laboratorio no existe.")
            elif e.pgcode == psycopg2.errorcodes.CHECK_VIOLATION:
                print("Salario debe ser positivo.")
            elif e.pgcode == psycopg2.errorcodes.NUMERIC_VALUE_OUT_OF_RANGE:
                print("Salario fuera de rango.")
            elif e.pgcode == psycopg2.errorcodes.INVALID_DATETIME_FORMAT:
                print("Formato de fecha incorrecto.")
            else:
                print(f"Erro: {e.pgcode} - {e.pgerror}")
            conn.rollback()


## ------------------------------------------------------------
# BAJA
def delete_worker(conn):
    id = input("Id del trabajador: ")
    id = None if id == '' else int(id)
    sql_query = """delete from Trabajadores where id = %s"""
    with conn.cursor() as curr:
        try:
            curr.execute(sql_query, (id,))
            if curr.rowcount == 0:
                print("Trabajador no encontrado")
            else:
                conn.commit()
                print("Trabajador eliminado")
        except psycopg2.Error as e:
            print(f"Erro: {e.pgcode} - {e.pgerror}")
            conn.rollback()


## ------------------------------------------------------------
# MODIFICACION
def update_salary(conn):
    id = input("Id del trabajador: ")
    id = None if id == '' else int(id)
    porcentaje = input("Porcentaje cambio: ")
    porcentaje = None if porcentaje == '' else float(porcentaje)
    sql_query = """update Trabajadores set salario = salario * (1 + %s/100) where id = %s"""
    with conn.cursor() as curr:
        try:
            curr.execute(sql_query, (porcentaje, id))
            if curr.rowcount == 0:
                print("Trabajador no encontrado")
            else:
                conn.commit()
                print("Salario actualizado")
        except psycopg2.Error as e:
            if e.pgcode == psycopg2.errorcodes.SERIALIZATION_FAILURE:
                print("No se puede modificar el salario porque ya ha sido modificado.")
            elif e.pgcode == psycopg2.errorcodes.CHECK_VIOLATION:
                print("El salario resultante debe ser positivo.")
            elif e.pgcode == psycopg2.errorcodes.NOT_NULL_VIOLATION:
                print("No puede haber nulos")
            else:
                print(f"Erro: {e.pgcode} - {e.pgerror}")
            conn.rollback()


## ------------------------------------------------------------
# SELECT
def show_workers_by_lab(conn):
    laboratorio = input("Id Laboratorio: ")
    laboratorio = None if laboratorio == '' else int(laboratorio)
    sql_query = """select * from Trabajadores where idLaboratorio = %s"""
    with conn.cursor(cursor_factory=psycopg2.extras.DictCursor) as curr:
        try:    
            curr.execute(sql_query, (laboratorio,))
            conn.commit()
            rows = curr.fetchall()
            for row in rows:
                print(f"Id: {row['id']}, Nombre: {row['nombre']}, Apellido1: {row['apellido1']}, Apellido2: {row['apellido2']}, Puesto: {row['puesto']}, Salario: {row['salario']}, Bonus: {row['bonus']}")
            print(f"{curr.rowcount} trabajadores")
        except psycopg2.Error as e:
            print(f"Erro: {e.pgcode} - {e.pgerror}")
            conn.rollback()

## ------------------------------------------------------------
# UPDATE
def change_capacity(conn):
    laboratorio = input("Id Laboratorio: ")
    laboratorio = None if laboratorio == '' else int(laboratorio)
    capacidad = input("Nueva Capacidad: ")
    capacidad = None if capacidad == '' else int(capacidad)
    sql_query = """update Laboratorio set capacidad = %s where id = %s"""
    with conn.cursor() as curr:
        try:
            curr.execute(sql_query, (capacidad, laboratorio))
            if curr.rowcount == 0:
                print("Laboratorio no encontrado")
            else:
                conn.commit()
                print("Capacidad actualizado")  
        except psycopg2.Error as e:
            if e.pgcode == psycopg2.errorcodes.CHECK_VIOLATION:
                print("La capacidad debe ser positiva.")
            elif e.pgcode == psycopg2.errorcodes.NOT_NULL_VIOLATION:
                print("No puede haber nulos")
            elif e.pgcode == psycopg2.errorcodes.SERIALIZATION_FAILURE:
                print("No se puede modificar la capacidad porque ya ha sido modificada.")
            else:
                print(f"Erro: {e.pgcode} - {e.pgerror}")
            conn.rollback()


## ------------------------------------------------------------
# SELECT
def show_labs_by_location(conn):
    localizacion = input("Id Localización: ")
    localizacion = None if localizacion == '' else int(localizacion)
    sql_query = """select * from Laboratorio where id = %s"""
    with conn.cursor(cursor_factory=psycopg2.extras.DictCursor) as curr:
        try:
            curr.execute(sql_query, (localizacion,))
            conn.commit()
            rows = curr.fetchall()
            for row in rows:
                print(f"Id: {row['id']}, Nombre: {row['nombre']}, Especialidad: {row['especialidad']}, Telefono: {row['telefono']}, Capacidad: {row['capacidad']}")
        except psycopg2.Error as e:
            print(f"Erro: {e.pgcode} - {e.pgerror}")
            conn.rollback()


## ------------------------------------------------------------
# 2 UPDATES
def give_bonus_to_workers(conn):
    trabajador1 = input("Id Trabajador a añadir bonus: ")
    trabajador1 = None if trabajador1 == '' else int(trabajador1)
    trabajador2 = input("Id Trabajador a quitar bonus: ")
    trabajador2 = None if trabajador2 == '' else int(trabajador2)
    bonus = input("Bonus: ")
    bonus = None if bonus == '' else float(bonus)
    sql_query = """update Trabajadores set bonus = bonus + %s where id in %s; 
                   update Trabajadores set bonus = bonus - %s where id in %s"""
    with conn.cursor() as curr:
        try:
            curr.execute(sql_query, (bonus, (trabajador1,), bonus, (trabajador2,)))
            conn.commit()
            print("Bonus actualizado")
        except psycopg2.Error as e:
            if e.pgcode == psycopg2.errorcodes.CHECK_VIOLATION:
                print("El bonus resultante no puede ser negativo.")
            elif e.pgcode == psycopg2.errorcodes.NOT_NULL_VIOLATION:
                print("No puede haber nulos")
            elif e.pgcode == psycopg2.errorcodes.SERIALIZATION_FAILURE:
                print("No se puede modificar el bonus porque otro usuario ya lo ha modificado.")
            else:
                print(f"Erro: {e.pgcode} - {e.pgerror}")
            conn.rollback()


## ------------------------------------------------------------
def menu(conn):
    MENU_TEXT = """
    1 - Añadir trabajador
    2 - Eliminar trabajador
    3 - Actualizar salario
    4 - Listar trabajadores por laboratorio
    5 - Listar laboratorios por localización
    6 - Transferir bonus de empleado eficiente
    7 - Cambiar capacidad de laboratorio
    q - Salir
    """

    while True:
        print(MENU_TEXT)
        opcion = input("Opción> ")
        if opcion == 'q':
            break
        elif opcion == '1':
            add_worker(conn)
        elif opcion == '2':
            delete_worker(conn)
        elif opcion == '3':
            update_salary(conn)
        elif opcion == '4':
            show_workers_by_lab(conn)
        elif opcion == '5':
            show_labs_by_location(conn)
        elif opcion == '6':
            give_bonus_to_workers(conn)
        elif opcion == '7':
            change_capacity(conn)
        else:
            print("Opción incorrecta")

## ------------------------------------------------------------
def main():
    """
    Función principal. Conecta á bd e executa o menú.
    Cando sae do menú, desconecta da bd e remata o programa
    """
    print('Conectando a PostgreSQL...')
    conn = connect_db()
    print('Conectado')
    menu(conn)
    disconnect_db(conn)


## ------------------------------------------------------------
if __name__ == '__main__':
    main()