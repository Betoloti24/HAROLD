# Clase de encuestas
class Encuestas():
    # Metodo constructor
    def __init__(self, id, nombre, descripcion):
        self.id = id
        self.nombre = nombre
        self.descripcion = descripcion
    
    # Metodo de impresion
    def __str__(self):
        return f"{self.nombre}\n\n"

# Clase para las categorias
class Categorias():
    # Metodo constructor
    def __init__(self, id, nombre):
        self.id = id
        self.nombre = nombre
        self.preguntas = []
    
    # Metodo de impresion
    def __str__(self):
        return f"{self.nombre}\n\n"

# Clase preguntas
class Preguntas():
    # Metodo constructor
    def __init__(self, id, descripcion):
        self.id = id
        self.descripcion = descripcion
        self.p100, self.p80, self.p60, self.p40, self.p20, self.nc, self.na = "", "", "", "", "", "", ""

    # Metodo de impresion
    def __str__(self):
        return f"{self.id}-{self.descripcion}\n"

    # Metodo para extraer una lista de preguntas
    def listpreguntas(request, preguntas, cookies):
        lpreguntas = []
        i = 0
        for pregunta in preguntas:
            # Obtenemos el resultado de la cookie
            cookie = cookies[i]
            i += 1
            # Convertimos la pregunta en objeto
            pregunta = Preguntas(pregunta[0], pregunta[1])
            pregunta.asignarcookies(cookie)

            # Ingresamos la pregunta en la lista
            lpreguntas.append(pregunta)

        return lpreguntas

    # Metodo para asignar los cookies
    def asignarcookies(self, respuesta):
        if (respuesta == f"81% - 100%"):
            self.p100, self.p80, self.p60, self.p40, self.p20, self.nc, self.na = "selected", "", "", "", "", "", ""
        elif (respuesta == f"61% - 80%"):
            self.p100, self.p80, self.p60, self.p40, self.p20, self.nc, self.na = "", "selected", "", "", "", "", ""
        elif (respuesta == f"41% - 60%"):
            self.p100, self.p80, self.p60, self.p40, self.p20, self.nc, self.na = "", "", "selected", "", "", "", ""
        elif (respuesta == f"21% - 40%"):
            self.p100, self.p80, self.p60, self.p40, self.p20, self.nc, self.na = "", "", "", "selected", "", "", ""
        elif (respuesta == f"0% - 20%"):
            self.p100, self.p80, self.p60, self.p40, self.p20, self.nc, self.na = "", "", "", "", "selected", "", ""
        elif (respuesta == f"N/C"):
            self.p100, self.p80, self.p60, self.p40, self.p20, self.nc, self.na = "", "", "", "", "", "selected", ""
        elif (respuesta == f"N/A"):
            self.p100, self.p80, self.p60, self.p40, self.p20, self.nc, self.na = "", "", "", "", "", "", "selected"

# Determinar si la encuesta fue respondida
def respencuesta(request, E):
    if (E in request.COOKIES):
        return True
    else:
        return False
