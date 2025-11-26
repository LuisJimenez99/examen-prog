from django.urls import path
from django.contrib.auth.views import LogoutView
from . import views

urlpatterns = [
    path('registro/', views.registro_view, name='registro'),
    path('login/', views.MiLoginView.as_view(), name='login'),
    path('logout/', LogoutView.as_view(next_page='login'), name='logout'),
]