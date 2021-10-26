from psycopg2 import connect

# Funcion para crear la BD en el SDB PostgreSQL
def createpostgresql():
    # Hacemos la conexion
    # conexion1 = connect(host="localhost", database="harold", user="postgres", password="2357", port=5432)

    conexion1 = connect(
        host="ec2-3-226-165-74.compute-1.amazonaws.com", 
        database="d1eu9mu6um7qb9", 
        user="wqzfdqensmcrma", 
        password="ddab0ec2daec0ee6ded7f296e58aa7af33d9ea17c6bde4147d9934e2dc53c19c", 
        port=5432)

    # Leemos el archivo .sql con todos los DDL para crear las Tablas y Constraint
    f = open("HAROLD\BD\DiseñoBD\Diseno.sql", "r", encoding="utf8")
    
    # Ejecutamos los DDL
    cursor1=conexion1.cursor()  # Movemos el apuntador
    cursor1.execute(f.read())   # Ejecutamos los DDL
    conexion1.commit()          # Guardamos los cambios
    conexion1.close()           # Cerramos la conexion

# Funcion para ingresar datos a la BD de Abastos
def insertpostgresql():
    # Hacemos la conexion
    # conexion1 = connect(host="localhost", database="harold", user="postgres", password="2357", port=5432)

    conexion1 = connect(
        host="ec2-3-226-165-74.compute-1.amazonaws.com", 
        database="d1eu9mu6um7qb9", 
        user="wqzfdqensmcrma", 
        password="ddab0ec2daec0ee6ded7f296e58aa7af33d9ea17c6bde4147d9934e2dc53c19c", 
        port=5432)

    # Leemos el archivo .sql con todos los DDL para insertar los datos en las Tablas
    f = open("HAROLD\BD\DiseñoBD\Datos.sql", "r", encoding="utf8")
    
    # Ejecutamos los DDL
    cursor1=conexion1.cursor()  # Movemos el apuntador
    cursor1.execute(f.read())   # Ejecutamos los DDL
    conexion1.commit()          # Guardamos los cambios
    conexion1.close()           # Cerramos la conexion

def consultar():
    conexion1 = connect(
        host="ec2-3-226-165-74.compute-1.amazonaws.com", 
        database="d1eu9mu6um7qb9", 
        user="wqzfdqensmcrma", 
        password="ddab0ec2daec0ee6ded7f296e58aa7af33d9ea17c6bde4147d9934e2dc53c19c", 
        port=5432)

    consulta = "SELECT * FROM categorias"
    # Ejecutamos los DDL
    cursor1=conexion1.cursor()  # Movemos el apuntador
    cursor1.execute(consulta)   # Ejecutamos los DDL
    
    resultado = cursor1.fetchall()

    print(len(resultado))

    for i in resultado:
        print(i)

    # Cerramos la conexion
    conexion1.close()           

# createpostgresql()
# insertpostgresql()

consultar()