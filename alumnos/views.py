from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic import ListView, CreateView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import login_required
from django.urls import reverse_lazy
from django.contrib import messages
from django.core.mail import EmailMessage
from django.conf import settings
import io

# ReportLab imports
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter

from .models import Alumno
from .forms import AlumnoForm

# 1. Dashboard
class DashboardView(LoginRequiredMixin, ListView):
    model = Alumno
    template_name = 'alumnos/dashboard.html'
    context_object_name = 'alumnos'

# 2. Crear Alumno
class AlumnoCreateView(LoginRequiredMixin, CreateView):
    model = Alumno
    form_class = AlumnoForm
    template_name = 'alumnos/crear_alumno.html'
    success_url = reverse_lazy('dashboard')

    def form_valid(self, form):
        messages.success(self.request, 'Alumno registrado correctamente.')
        return super().form_valid(form)

# 3. PDF Individual
@login_required
def enviar_reporte_pdf(request, pk):
    alumno = get_object_or_404(Alumno, pk=pk)
    buffer = io.BytesIO()
    p = canvas.Canvas(buffer, pagesize=letter)
    
    # Dibujamos al alumno
    _dibujar_alumno_en_pdf(p, alumno)
    p.showPage()
    p.save()
    
    pdf_content = buffer.getvalue()
    buffer.close()

    _enviar_email_pdf(
        request, 
        f"Reporte Individual: {alumno.nombre}", 
        f"Ficha_{alumno.legajo}.pdf", 
        pdf_content
    )
    return redirect('dashboard')

# 4. PDF MASIVO (NUEVO) 🚀
@login_required
def enviar_todos_pdf(request):
    alumnos = Alumno.objects.all()
    
    if not alumnos:
        messages.warning(request, "No hay alumnos para generar el reporte.")
        return redirect('dashboard')

    buffer = io.BytesIO()
    p = canvas.Canvas(buffer, pagesize=letter)

    # Recorremos todos los alumnos
    for alumno in alumnos:
        _dibujar_alumno_en_pdf(p, alumno)
        p.showPage() # ¡Esto crea una página nueva en el PDF!

    p.save()
    pdf_content = buffer.getvalue()
    buffer.close()

    _enviar_email_pdf(
        request, 
        f"Reporte General de Alumnos ({len(alumnos)})", 
        "Reporte_Completo_Alumnos.pdf", 
        pdf_content
    )
    return redirect('dashboard')


# --- FUNCIONES AUXILIARES (Para no repetir código) ---

def _dibujar_alumno_en_pdf(p, alumno):
    """Dibuja los datos de un alumno en la página actual del canvas"""
    p.setFont("Helvetica-Bold", 20)
    p.drawString(100, 750, "Ficha de Alumno")
    
    p.setFont("Helvetica", 12)
    p.drawString(100, 700, f"Nombre: {alumno.nombre} {alumno.apellido}")
    p.drawString(100, 680, f"Legajo: {alumno.legajo}")
    p.drawString(100, 660, f"Carrera: {alumno.carrera}")
    p.drawString(100, 640, f"Contacto: {alumno.email}")
    
    p.line(100, 620, 500, 620)
    p.drawString(100, 600, "Documento generado automáticamente por Sistema Django.")

def _enviar_email_pdf(request, asunto, nombre_archivo, contenido_pdf):
    """Se encarga de adjuntar y enviar el correo"""
    email = EmailMessage(
        asunto,
        "Adjuntamos el reporte solicitado desde el panel de gestión.",
        settings.DEFAULT_FROM_EMAIL,
        [request.user.email],
    )
    email.attach(nombre_archivo, contenido_pdf, 'application/pdf')
    
    try:
        email.send()
        messages.success(request, f'Se ha enviado "{asunto}" a tu correo.')
    except Exception as e:
        print(f"Error enviando PDF: {e}")
        messages.error(request, 'Error al enviar el correo. Verifica la configuración.')