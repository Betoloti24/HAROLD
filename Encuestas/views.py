from django import http
from django.shortcuts import render
from django.urls import reverse_lazy
from django.http import HttpResponseRedirect
from .models import Preguntas, respencuesta
from HAROLD.BD.AdmBD.Encuestas import buscarencuesta, buscarcategoria, buscarpreguntas, ingresarcuestionario

# Vista del menu de encuestas
def menu(request):
    # Verificamos la existencia de la entrada
    if ('entrada' in request.COOKIES):
        entrada = False
    else:
        entrada = True

    # Verificamos que encuestas ya se realizaron
    E1 = respencuesta(request, "E1")
    E2 = respencuesta(request, "E2")
    E3 = respencuesta(request, "E3")
    E4 = respencuesta(request, "E4")
    E5 = respencuesta(request, "E5")

    # Verificamos si se ha realizado algun metodo post
    if (request.method == "POST"):
        listE = [request.COOKIES["E1"], request.COOKIES["E2"], request.COOKIES["E3"], request.COOKIES["E4"], request.COOKIES["E5"]]
        ci = request.COOKIES["ci"]
        ingresarcuestionario(request, listE, ci)
        url = str(reverse_lazy("final"))
        return HttpResponseRedirect(url)

    # Verificamos que todas las encuestas esten completadas
    if (E1 and E2 and E3 and E4 and E5):
        guardar = True
    else:
        guardar = False

    # Declaramos el contexto
    contexto = {
        'entrada': entrada,
        'nombre': request.COOKIES['nombre'],
        'E1': E1,
        'E2': E2,
        'E3': E3,
        'E4': E4,
        'E5': E5,
        'guardar': guardar,
    }

    http = render(request, "menu.html", contexto)

    # Cramos el cookie de entrada si se necesita
    if (entrada):
        http.set_cookie('entrada', 'true')

    # Enviamos el http
    return http

# Vista de la encuesta
def encuestas(request, encuesta):
    dencuesta = buscarencuesta(request, f"E{encuesta}")      # Buscamos la encuesta actual
    categorias = buscarcategoria(request, f"E{encuesta}")    # Buscamos las categorias de la encuesta

    # Verificamos si existen valores de la encuesta
    if (f"E{encuesta}" in request.COOKIES):
        E = request.COOKIES[f"E{encuesta}"]
        E = E.split("|")
        obs = E[-1]
    else:
        obs = ""

    # Ingresamos las preguntas a la categoria
    categorias = buscarpreguntas(request, categorias, f"E{encuesta}")            

    # Verificamos si se manda un metodo POST
    errFalta, errObs, mensaje, cookie = False, False, "", ""
    if (request.method == "POST"):
        # Extraemos las observaciones
        obs = request.POST["observaciones"]
        for cat in categorias:
            for pre in cat.preguntas:
                # Extraemos la respuesta a la pregunta
                buscar = f"porcentaje{pre.id}"
                respuesta = request.POST[buscar]

                # Guardamos la informacion suministrada para no eliminar la antes ingresada
                pre.asignarcookies(respuesta)

                # Validamos que no haya una pregunta sin responder
                if (respuesta == "Seleccionar" and not errFalta):    
                    errFalta = True
                    mensaje = f"La categoría '{cat.nombre}' tiene una pregunta sin responder"

                # Validamos si hay obs N/A o N/C y sin observaciones
                elif ((respuesta in ["N/A", "N/C"]) and obs == "" and not errFalta):
                    errObs = True
                    mensaje = f"Se tiene en la categoria '{cat.nombre}' una respuesta con N/C o N/A; se requieren observaciones sí califica con dichos niveles"
                else:
                    cookie = f"{cookie}|{respuesta}"
        if (not errObs and not errFalta):
            # Ingresamos la observacion a la cookie
            cookie = f"{cookie[1:]}|{obs}"

            # Declaramos el obj http del menu
            url = str(reverse_lazy("menu"))
            http = HttpResponseRedirect(url)
            
            # Ingresamos la cookie en el http de menu
            http.set_cookie(f"E{encuesta}", cookie)
            return http

    # Declaramos y asignamos el contexto
    contexto = {
        'encuesta': dencuesta,
        'categorias': categorias,
        'mensaje': mensaje,
        'errFalta': errFalta,
        'errObs': errObs,
        'obs': obs
    }

    return render(request, "encuesta.html", contexto)

# Vista final de la encuesta 
def final(request):
    return render(request, "final.html")