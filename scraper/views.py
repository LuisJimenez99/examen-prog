import requests
from bs4 import BeautifulSoup
from django.shortcuts import render, redirect
from django.contrib import messages
from django.core.mail import send_mail
from django.conf import settings
from django.contrib.auth.decorators import login_required


@login_required
def buscar_view(request):
    data = None
    query = request.GET.get('q')

    if query:
        url = f"https://es.wikipedia.org/wiki/{query.replace(' ', '_')}"
        
        try:
            headers = {'User-Agent': 'Mozilla/5.0'}
            response = requests.get(url, headers=headers, timeout=5)

            if response.status_code == 200:
                soup = BeautifulSoup(response.text, 'html.parser')

                
                titulo_tag = soup.find('h1', {'id': 'firstHeading'})
                titulo = titulo_tag.text if titulo_tag else query

                
                resumen = "No se encontró descripción."
                contenido = soup.find('div', {'id': 'bodyContent'})
                if contenido:
                    parrafos = contenido.find_all('p')
                    for p in parrafos:
                        if len(p.text) > 50:
                            resumen = p.text
                            break
                
                
                imagen_url = None
                
                infobox = soup.find('table', {'class': 'infobox'})
                if infobox:
                    img_tag = infobox.find('img')
                    if img_tag:
                        imagen_url = img_tag.get('src')
                
                
                if not imagen_url:
                    thumb = soup.find('div', {'class': 'tright'})
                    if thumb:
                        img_tag = thumb.find('img')
                        if img_tag:
                            imagen_url = img_tag.get('src')

                
                if imagen_url and imagen_url.startswith('//'):
                    imagen_url = f"https:{imagen_url}"
                
                data = {
                    'titulo': titulo,
                    'resumen': resumen,
                    'url': url,
                    'imagen': imagen_url 
                }
            else:
                messages.error(request, f"No encontramos resultados para '{query}' en Wikipedia.")
        
        except Exception as e:
            messages.error(request, "Error de conexión con Wikipedia.")

    return render(request, 'scraper/buscar.html', {'data': data, 'query': query})


@login_required
def enviar_investigacion(request):
    if request.method == 'POST':
        titulo = request.POST.get('titulo')
        resumen = request.POST.get('resumen')
        url_fuente = request.POST.get('url')
        imagen_src = request.POST.get('imagen') 
        
        asunto = f"Investigación: {titulo}"
        mensaje = f"""
        Hola {request.user.username},
        
        Aquí tienes el resultado de tu investigación:
        
        TEMA: {titulo}
        ----------------------------------------------------
        {resumen}
        ----------------------------------------------------
        
        Foto principal: {imagen_src if imagen_src else 'No disponible'}
        Fuente original: {url_fuente}
        
        Saludos,
        Sistema de Alumnos
        """
        
        try:
            send_mail(
                asunto,
                mensaje,
                settings.EMAIL_HOST_USER,
                [request.user.email],
                fail_silently=False,
            )
            messages.success(request, "La información (con foto) fue enviada a tu correo.")
        except Exception as e:
            messages.error(request, "Error al enviar el correo.")
            
    return redirect('buscador')