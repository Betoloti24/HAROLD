from psycopg2 import connect
from Encuestas.models import Categorias, Preguntas, Encuestas
from datetime import date

# Buscar datos de encuestas
def buscarencuesta(request, id):
    # Hacer la conexion
    conexion = connect(
        host=request.COOKIES['host'], 
        user=request.COOKIES['user'], 
        password=request.COOKIES['password'], 
        database=request.COOKIES['database'], 
        port=request.COOKIES['port'])
    cursor = conexion.cursor()

    # Declarar consulta
    consulta = f"SELECT * FROM encuestas WHERE codigo = '{id}'"

    # Hacemos la consulta
    cursor.execute(consulta)
    resultado = cursor.fetchall()
    resultado = resultado[0]

    # Cerramos la conexion
    conexion.close()           

    # Retornamos el usuario buscado
    return Encuestas(resultado[0], resultado[1], resultado[2])

# Buscar categorias de una encuesta
def buscarcategoria(request, id):
    # Hacer la conexion
    conexion = connect(
        host=request.COOKIES['host'], 
        user=request.COOKIES['user'], 
        password=request.COOKIES['password'], 
        database=request.COOKIES['database'], 
        port=request.COOKIES['port'])
    cursor = conexion.cursor()

    # Declarar consulta
    consulta = f"SELECT * FROM categorias WHERE encuesta = '{id}'"

    # Hacemos la consulta
    cursor.execute(consulta)
    resultado = cursor.fetchall()

    # Cerramos la conexion
    conexion.close()      

    # Retornamos el usuario buscado
    return resultado

# Buscamos las preguntas de las categorias
def buscarpreguntas(request, categorias, encuesta):
    # Estructuras a utilizar
    lpreguntas = [] 
    resultado = []

    # Hacer la conexion
    conexion = connect(
        host=request.COOKIES['host'], 
        user=request.COOKIES['user'], 
        password=request.COOKIES['password'], 
        database=request.COOKIES['database'], 
        port=request.COOKIES['port'])
    cursor = conexion.cursor()

    if (encuesta in request.COOKIES):
        E = request.COOKIES[encuesta]
        E = E.split('|')

    for categoria in categorias:
        # Convertimos la categoria en objeto
        categoria = Categorias(categoria[0], categoria[1])

        # Declarar consulta
        consulta = f"SELECT * FROM preguntas WHERE categoria = '{categoria.id}'"

        # Hacemos la consulta
        cursor.execute(consulta)
        preguntas = cursor.fetchall()

        # Obtenemos las cookies para esta categoria
        if (encuesta in request.COOKIES):
            cookies = E[:len(preguntas)]
            E = E[len(preguntas):]
        else:
            cookies = [""]*len(preguntas)

        # Obtenemos una lista de preguntas
        lpreguntas = Preguntas.listpreguntas(request, preguntas, cookies)

        # Ingresamos la lista a la categoria
        categoria.preguntas = lpreguntas

        # Ingresamos las preguntas a la categoria
        resultado.append(categoria)

    # Cerramos la conexion
    conexion.close()

    # Retornamos la categiroa con su lista de objetos
    return resultado

# Ingresamos los resultados del cuestionario
def ingresarcuestionario(request, listaE, ci):
    # Variables a utilizar
    encuesta, respuestas, pregunta, fecha, obs = [], "", "", date.today(), ""
    indice = 1
    # Vamos Guardando la info encuesta por encuesta
    for E in listaE:
        # Extraemos los datos de la encuesta
        encuesta = E.split("|")
        obs = encuesta[-1]
        respuestas = encuesta[:len(encuesta)-1]

        # Creamos el registro de respuesta encuesta
        reg_encuesta = (fecha, f"E{indice}", ci, obs)

        # Ingresamos el registro
        encuesta = ingresarencuesta(request, reg_encuesta, f"E{indice}")
        
        # Generamos la lista de respuesta
        regs_respuestas = []
        pregunta, j = asignarpregunta(indice), 1
        
        for aceptacion in respuestas:
            tupla_resp = (aceptacion, encuesta, f"{pregunta}{j}")
            regs_respuestas.append(tupla_resp)
            j += 1

        # Ingresamos las respuestas a la tabla de respuestas
        asignarrespuestas(request, regs_respuestas)

        indice += 1
        
# Determinamos la preposicion que debe de tener la pregunta
def asignarpregunta(indice):
    if (indice == 1):
        return "R"
    elif (indice == 2):
        return "P"
    elif (indice == 3):
        return "S"
    elif (indice == 4):
        return "F"
    else:
        return "L"

# Ingresamos la encuesta
def ingresarencuesta(request, registro, encuesta):
    # Hacer la conexion
    # conexion = connect(host="localhost", database="harold", user="postgres", password="2357", port=5432)
    conexion = connect(
        host=request.COOKIES['host'], 
        user=request.COOKIES['user'], 
        password=request.COOKIES['password'], 
        database=request.COOKIES['database'], 
        port=request.COOKIES['port'])
    cursor = conexion.cursor()

    # Declarar consulta
    consulta = f"INSERT INTO respuestas_e(fecha, encuesta, usuario, observacion) VALUES ('{registro[0]}', '{registro[1]}', '{registro[2]}', '{registro[3]}')"

    # Hacemos la consulta
    cursor.execute(consulta)
    # Mantenemos los cambios
    conexion.commit()

    # Consultamos el registro que se ingresó
    consulta = f"SELECT cod FROM respuestas_e WHERE fecha = '{registro[0]}' and usuario = '{registro[2]}' and encuesta = '{encuesta}'"

    # Hacemos la consulta
    cursor.execute(consulta)
    respuesta = cursor.fetchall()

    # Cerramos la conexion
    conexion.close()

    return respuesta[0][0]

# Ingresamos las respuestas
def asignarrespuestas(request, registros):
    # Hacer la conexion
    # conexion = connect(host="localhost", database="harold", user="postgres", password="2357", port=5432)
    conexion = connect(
        host=request.COOKIES['host'], 
        user=request.COOKIES['user'], 
        password=request.COOKIES['password'], 
        database=request.COOKIES['database'], 
        port=request.COOKIES['port'])
    cursor = conexion.cursor()

    # Ingresamos todas las respuestas
    for reg in registros:
        # Declarar consulta
        consulta = f"INSERT INTO respuestas(p_aceptacion, encuesta, pregunta) VALUES ('{reg[0]}', {reg[1]}, '{reg[2]}')"

        # Hacemos la consulta
        cursor.execute(consulta)
    
    # Mantenemos los cambios
    conexion.commit()

    # Cerramos la conexion
    conexion.close()
    