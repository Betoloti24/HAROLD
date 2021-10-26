from django.urls import path, include
from .views import registro, bienvenida

urlpatterns = [
    path('', bienvenida, name="bienvenida"),
    path('registro/', registro, name="registro"),
]