from django.urls import path
from . import views

urlpatterns = [
    path('buscar/', views.buscar_view, name='buscador'),
    path('enviar/', views.enviar_investigacion, name='enviar_investigacion'),
]