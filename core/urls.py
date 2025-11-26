from django.contrib import admin
from django.urls import path, include
from usuarios.views import home_view # <--- Importamos la nueva vista

urlpatterns = [
path('admin/', admin.site.urls),
path('usuarios/', include('usuarios.urls')),
path('alumnos/', include('alumnos.urls')),
path('investigacion/', include('scraper.urls')),
path('', home_view, name='home'),


]