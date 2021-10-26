from os import name
from django.urls import path, include
from .views import encuestas, menu, final

urlpatterns = [
    path('encuestas/<int:encuesta>', encuestas, name="encuestas"),
    path('menu/', menu, name='menu'),
    path('final/', final, name='final'),
]