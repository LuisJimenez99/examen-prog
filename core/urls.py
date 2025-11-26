from django.contrib import admin
from django.urls import path, include
from django.views.generic import RedirectView 

urlpatterns = [
    
    path('admin/', admin.site.urls),
    path('usuarios/', include('usuarios.urls')),
    path('alumnos/', include('alumnos.urls')),
    path('investigacion/', include('scraper.urls')),
    path('', RedirectView.as_view(url='/alumnos/dashboard/', permanent=False), name='home'),
]