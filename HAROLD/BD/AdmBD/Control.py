from django.urls import reverse_lazy
from django.http import HttpResponseRedirect

# Funcion para estableces la BD de desarrollo
def desarrollo(http):
    http.set_cookie('host', 'localhost')
    http.set_cookie('user', 'postgres')
    http.set_cookie('password', '2357')
    http.set_cookie('database', 'harold')
    http.set_cookie('port', '5432')

# Funcion para establecer la BD de produccion
def produccion(http):
    http.set_cookie('host', 'ec2-3-226-165-74.compute-1.amazonaws.com')
    http.set_cookie('user', 'wqzfdqensmcrma')
    http.set_cookie('password', 'ddab0ec2daec0ee6ded7f296e58aa7af33d9ea17c6bde4147d9934e2dc53c19c')
    http.set_cookie('database', 'd1eu9mu6um7qb9')
    http.set_cookie('port', '5432')