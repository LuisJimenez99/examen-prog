from django.shortcuts import render, redirect
from django.contrib.auth import login
from django.contrib.auth.views import LoginView, LogoutView
from django.core.mail import send_mail
from django.conf import settings
from django.contrib import messages
from .forms import RegistroForm

def registro_view(request):
    if request.user.is_authenticated:
        return redirect('home')

    if request.method == 'POST':
        form = RegistroForm(request.POST)
        if form.is_valid():
            user = form.save()
            
            try:
                send_mail(
                    subject='¡Bienvenido a la Plataforma!',
                    message=f'Hola {user.username}, gracias por registrarte en nuestro sistema de alumnos.',
                    from_email=settings.EMAIL_HOST_USER,
                    recipient_list=[user.email],
                    fail_silently=False,
                )
            except Exception as e:
                print(f"Error enviando mail: {e}")

            login(request, user)
            messages.success(request, 'Registro exitoso. Te hemos enviado un correo.')
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