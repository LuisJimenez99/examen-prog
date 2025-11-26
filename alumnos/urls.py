from django.urls import path
from .views import DashboardView, AlumnoCreateView, enviar_reporte_pdf

urlpatterns = [
    path('dashboard/', DashboardView.as_view(), name='dashboard'),
    path('nuevo/', AlumnoCreateView.as_view(), name='crear_alumno'),
    path('enviar-pdf/<int:pk>/', enviar_reporte_pdf, name='enviar_pdf'),
]