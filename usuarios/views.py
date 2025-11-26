from django.shortcuts import render, redirect
from django.contrib.auth import login
from django.contrib.auth.views import LoginView
from django.core.mail import send_mail
from django.conf import settings
from django.contrib import messages
from .forms import RegistroForm

# Importaciones para el gráfico del Home
from django.db.models import Count
from alumnos.models import Alumno
import json

def registro_view(request):
    if request.user.is_authenticated:
        return redirect('home')

    if request.method == 'POST':
        form = RegistroForm(request.POST)
        if form.is_valid():
            user = form.save()
            
            # --- ENVÍO DE CORREO DE BIENVENIDA ---
            try:
                print("Intentando enviar email de bienvenida...")
                
                send_mail(
                    subject='¡Registro Exitoso! - Sistema de Alumnos',
                    message=f"""
                    Estimado/a {user.username},

                    ¡Muchas gracias por registrarte en nuestra plataforma!

                    Este correo es una confirmación automática para verificar que tu cuenta ha sido creada correctamente en la base de datos del sistema.

                    -------------------------------------------------------------
                    ✅ VERIFICACIÓN DE EXAMEN DE PROGRAMACIÓN
                    -------------------------------------------------------------
                    Si estás leyendo esto, significa que el sistema de envío de correos (integrado con SendGrid) y el despliegue en la nube (Render) están funcionando perfectamente.
                    
                    A partir de ahora puedes:
                    1. Iniciar sesión en el panel.
                    2. Gestionar alumnos.
                    3. Generar reportes PDF y recibirlos por aquí.

                    ¡Esperamos que tengas una excelente experiencia!

                    Atentamente,
                    El Equipo de Desarrollo (Examen Final)
                    """,
                    
                    from_email=settings.DEFAULT_FROM_EMAIL, 
                    recipient_list=[user.email],
                    fail_silently=False,
                )
                print("Email de bienvenida enviado con éxito.")
                
            except Exception as e:
                print(f"⚠️ Error enviando mail de registro: {e}")
                # No interrumpimos el flujo si falla el mail

            login(request, user)
            messages.success(request, 'Registro exitoso. Te hemos enviado un correo de confirmación.')
            return redirect('home')
    else:
        form = RegistroForm()
    
    return render(request, 'usuarios/registro.html', {'form': form})

class MiLoginView(LoginView):
    template_name = 'usuarios/login.html'
    
    def get_form(self, form_class=None):
        form = super().get_form(form_class)
        for field in form.fields:
            form.fields[field].widget.attrs.update({
                'class': 'form-control bg-dark text-white border-secondary'
            })
        return form


def home_view(request):
    
    if not request.user.is_authenticated:
        return render(request, 'usuarios/home.html')

    
    datos_carreras = (
        Alumno.objects
        .values('carrera')
        .annotate(total=Count('id'))
        .order_by('-total')
    )

    labels = [item['carrera'] for item in datos_carreras]
    data = [item['total'] for item in datos_carreras]

    context = {
        'labels_json': json.dumps(labels),
        'data_json': json.dumps(data),
        'total_alumnos': Alumno.objects.count()
    }

    return render(request, 'usuarios/home.html', context)