from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic import ListView, CreateView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import login_required
from django.urls import reverse_lazy
from django.contrib import messages
from django.core.mail import EmailMessage
from django.conf import settings
import io

from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter

from .models import Alumno
from .forms import AlumnoForm

class DashboardView(LoginRequiredMixin, ListView):
    model = Alumno
    template_name = 'alumnos/dashboard.html'
    context_object_name = 'alumnos'

class AlumnoCreateView(LoginRequiredMixin, CreateView):
    model = Alumno
    form_class = AlumnoForm
    template_name = 'alumnos/crear_alumno.html'
    success_url = reverse_lazy('dashboard')

    def form_valid(self, form):
        messages.success(self.request, 'Alumno registrado correctamente.')
        return super().form_valid(form)

@login_required
def enviar_reporte_pdf(request, pk):
    alumno = get_object_or_404(Alumno, pk=pk)

    buffer = io.BytesIO()
    p = canvas.Canvas(buffer, pagesize=letter)
    
    p.setFont("Helvetica-Bold", 20)
    p.drawString(100, 750, "Ficha de Alumno")
    
    p.setFont("Helvetica", 12)
    p.drawString(100, 700, f"Nombre: {alumno.nombre} {alumno.apellido}")
    p.drawString(100, 680, f"Legajo: {alumno.legajo}")
    p.drawString(100, 660, f"Carrera: {alumno.carrera}")
    p.drawString(100, 640, f"Contacto: {alumno.email}")
    
    p.line(100, 620, 500, 620)
    p.drawString(100, 600, "Documento generado automáticamente por Sistema Django.")
    
    p.showPage()
    p.save()
    
    pdf_content = buffer.getvalue()
    buffer.close()

    subject = f"Reporte de Alumno: {alumno.nombre} {alumno.apellido}"
    body = "Adjuntamos la ficha técnica del alumno solicitada desde el sistema."
    email_destino = request.user.email  

    email = EmailMessage(
        subject,
        body,
        settings.EMAIL_HOST_USER,
        [email_destino],
    )
    
    email.attach(f'Ficha_{alumno.legajo}.pdf', pdf_content, 'application/pdf')

    try:
        email.send()
        messages.success(request, f'Se ha enviado el PDF de {alumno.nombre} a tu correo ({email_destino}).')
    except Exception as e:
        messages.error(request, f'Error al enviar el correo: {e}')

    return redirect('dashboard')