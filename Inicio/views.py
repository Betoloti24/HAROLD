from django.shortcuts import render
from django.urls import reverse_lazy
from django.http import HttpResponseRedirect
from HAROLD.BD.AdmBD.Usuarios import buscar, ingresar, buscaruser
from HAROLD.BD.AdmBD.Control import desarrollo, produccion
from HAROLD.settings import DEBUG

# Vista para la bienvenida
def bienvenida(request):
    # Verificamos si se ha dejado una encuesta a la mitad
    cookies, mensaje = request.COOKIES, ""
    if ('E1' in cookies or 'E2' in cookies or 'E3' in cookies or 'E4' in cookies or 'E5' in cookies):
        smscookies, mensaje, Error = True, "Usted tiene un cuestionario en curso, ¿Desea retomarlo nuevamente?", "Error"
    else:
        smscookies, mensaje, Error = False, "", "Aviso de Cuestionario en Curso"

    Error = False
    if request.method == "POST":    # Verificamos si se ha enviado un metodo POST
        opcion = request.POST["opcion"]
        if (opcion == "ingresar"):
            try:
                cedula = int((request.POST["cedula"]))  # Convertimos a entero el info ingresada en cedula
                # Verificamos si la cedula ingresada es correcta
                if (cedula >= 1000000 and cedula < 40000000):
                    if (buscar(request, cedula)):
                        url = str(reverse_lazy(('menu'))) # Determinamos la URL de la encuesta
                        http = HttpResponseRedirect(url)
                        http.set_cookie('nombre', str(buscaruser(request, cedula)))     # Ingresamos la cookie del nombre del usuario
                        return http
                    else:
                        url = str(reverse_lazy(('registro')))   # Determinamos la URL del registro
                        http = HttpResponseRedirect(url)
                        http.set_cookie('ci', str(cedula))
                        return http
                else:
                    Error = True
                    mensaje = "La cédula ingresada no es válida"
            except ValueError:
                Error = True
                mensaje = "Debe de ingresar sólo números enteros"
        elif (opcion == "si"):
            # Nos vamos directamente al menu de encuestas
            url = str(reverse_lazy("menu"))
            return HttpResponseRedirect(url)
        else:
            # Declaramos el obj http de la bienvenida
            http = render(request, "bienvenida.html")
            # Eliminamos las cookies
            http.delete_cookie("E1")
            http.delete_cookie("E2")
            http.delete_cookie("E3")
            http.delete_cookie("E4")
            http.delete_cookie("E5")
            # Volvemos a renderizar
            return http

    contexto = {
        'Error': Error,
        'smscookies': smscookies,
        'mensaje': mensaje,
    }

    # Determinamos las configuraciones del servidor de BD (Desarrollo, Produccion)
    http = render(request, "bienvenida.html", contexto)

    if (DEBUG):
        desarrollo(http)
    else:
        produccion(http)

    # Verificamos si existe la llave de entrada
    if ('entrada' in request.COOKIES):
        http.delete_cookie('entrada')

    return http

# Vista para el registro
def registro(request):
    if request.method == "POST":    # Verificamos si se ha enviado un metodo POST
        nombre, apellido, usuario = [request.POST['nombre'], request.POST['apellido'], request.POST['usuario']]   # Guardamos los datos del formulario
        correo = f"{usuario}@bod.com.ve"                    # Generamos el correo por medio del usuario
        ci = request.COOKIES['ci']                          # Extraemos lo cookies
        ingresar(request, ci, nombre, apellido, correo)     # Ingresamos al usuario
        url = str(reverse_lazy('menu'))
        http = HttpResponseRedirect(url)
        http.set_cookie('nombre', nombre)
        return http
    return render(request, "registro.html")
