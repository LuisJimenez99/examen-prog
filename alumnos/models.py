from django.db import models

class Alumno(models.Model):
        nombre = models.CharField(max_length=100)
        apellido = models.CharField(max_length=100)
        legajo = models.CharField(max_length=20, unique=True, verbose_name="Número de Legajo")
        email = models.EmailField(verbose_name="Email del Alumno")
        carrera = models.CharField(max_length=100, default="Desarrollo Web")
        fecha_creacion = models.DateTimeField(auto_now_add=True)

        def __str__(self):
            return f"{self.apellido}, {self.nombre}"
        
        class Meta:
            ordering = ['-fecha_creacion']