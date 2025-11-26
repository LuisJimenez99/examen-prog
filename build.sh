#!/usr/bin/env bash
# exit on error
set -o errexit

# --- TRUCO: Instalar Gunicorn explícitamente primero ---
pip install gunicorn

# Instalar el resto de librerías
pip install -r requirements.txt

# Recolectar archivos estáticos
python manage.py collectstatic --no-input

# Ejecutar migraciones
python manage.py migrate