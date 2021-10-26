from psycopg2 import connect

# Metodo para buscar un usuario
def buscar(request, id):
    # Hacer la conexion
    conexion = connect(
        host=request.COOKIES['host'], 
        user=request.COOKIES['user'], 
        password=request.COOKIES['password'], 
        database=request.COOKIES['database'], 
        port=request.COOKIES['port'])
    cursor = conexion.cursor()

    # Declarar consulta
    consulta = f"SELECT * FROM usuarios WHERE cedula = '{id}'"

    # Hacemos la consulta
    cursor.execute(consulta)
    resultado = cursor.fetchall()

    # Cerramos la conexion
    conexion.close()

    # Retornamos el usuario buscado
    return len(resultado) == 1

# Metodo para ingresar un usuario
def ingresar(request, ci, nombre, apellido, correo):
    # Hacer la conexion
    conexion = connect(
        host=request.COOKIES['host'], 
        user=request.COOKIES['user'], 
        password=request.COOKIES['password'], 
        database=request.COOKIES['database'], 
        port=request.COOKIES['port'])
    cursor = conexion.cursor()

    # Declarar consulta
    consulta = f"INSERT INTO usuarios VALUES ('{ci}', '{nombre}', '{apellido}', '{correo}')"

    # Hacemos la consulta
    cursor.execute(consulta)
    conexion.commit()

    # Cerramos la conexion
    conexion.close()

# Metodo para buscar el nombre de un usuario
def buscaruser(request, id):
    # Hacer la conexion
    conexion = connect(
        host=request.COOKIES['host'], 
        user=request.COOKIES['user'], 
        password=request.COOKIES['password'], 
        database=request.COOKIES['database'], 
        port=request.COOKIES['port'])
    cursor = conexion.cursor()

    # Declarar consulta
    consulta = f"SELECT nombre FROM usuarios WHERE cedula = '{id}'"

    # Hacemos la consulta
    cursor.execute(consulta)
    resultado = cursor.fetchall()

    # Cerramos la conexion
    conexion.close()

    # Retornamos el usuario buscado
    return resultado[0][0]