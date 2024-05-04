import psycopg2
import psycopg2.extras
import psycopg2.extensions
import psycopg2.errorcodes

## ------------------------------------------------------------
def connect_db():
    conn = psycopg2.connect("")
    conn.autocommit = False
    return conn


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
    nombre = input("Nombre del trabajador: ")
    apellido2 = input("Primer apellido: ")
    apellido2 = input("Segundo apellido: ")
    fechaNacimiento = input("Fecha Nacimiento: ")
    fechaAlta = input("Fecha Alta: ")
    puesto = input("Puesto: ")
    salario = input("Salario: ")
    salario = None if salario == '' else float(salario)
    laboratorio = input("Laboratorio: ")
    laboratorio = None if laboratorio == '' else int(laboratorio)

    sql_query = """insert into Trabajadores(id, dni, nombre, apellido1, apellido2, fechaNacimiento, fechaAlta, puesto, salario, idLaboratorio) 
                   values(%(id)s, %(dni)s, %(n)s, %(a1)s, %(a2)s, %(fn)s, %(fa)s, %(p)s, %(s)s, %(idl)s)"""
    with conn.cursor() as curr:
        try: 
            curr.execute(sql_query, {'id': id, 'dni': dni, 'n': nombre, 'a1': a1, 'a2': a2, 'fn': fechaNacimiento, 'fa': fechaAlta, 'p': puesto, 's': salario, 'idl': idLaboratorio})
            conn.commit()
            print("Trabajador añadido")
        except psycopg2.Error as :
            if e.pgcode == psycopg2.errorcodes.UNIQUE_VIOLATION:
                print("O traballador xa existe")
            else:
                print(f"Erro: {e.pgcode} - {e.pgerror}")
            conn.rollback()


## ------------------------------------------------------------
# BAJA
def delete_worker(conn):
    id = input("Id del trabajador: ")
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
    porcentaje = input("Porcentaje cambio: ")
    porcentaje = None if porcentaje == '' else float(salario)
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
                print(f"{row['id']} - {row['nombre']} {row['apellido1']} {row['apellido2']} - {row['puesto']} - {row['salario']}")
        except psycopg2.Error as e:
            print(f"Erro: {e.pgcode} - {e.pgerror}")
            conn.rollback()


## ------------------------------------------------------------
# SELECT
def show_labs_by_location(conn):
    localizacion = input("Localización: ")
    sql_query = """select * from Laboratorios where localizacion = %s"""
    with conn.cursor(cursor_factory=psycopg2.extras.DictCursor) as curr:
        try:
            curr.execute(sql_query, (localizacion,))
            conn.commit()
            rows = curr.fetchall()
            for row in rows:
                print(f"{row['id']} - {row['nombre']} - {row['especialidad']} - {row['localizacion']}")
        except psycopg2.Error as e:
            print(f"Erro: {e.pgcode} - {e.pgerror}")
            conn.rollback()


## ------------------------------------------------------------
def menu(conn):
    MENU_TEXT = """
    1 - Añadir trabajador
    2 - Eliminar trabajador
    3 - Actualizar salario
    4 - Listar trabajadores por laboratorio
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