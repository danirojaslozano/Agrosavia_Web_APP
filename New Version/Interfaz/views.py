from django.shortcuts import render,redirect,render_to_response
from django.http import HttpResponse,StreamingHttpResponse
from django.http import Http404

# Create your views here.

LISTA_ACTIVIDADES = ['Comiendo', 'Rumiando', 'Tomando Agua', 'Durmiendo', 'Caminando', 'Nada']
LISTA_LINKS = ['comiendo.png', 'rumia.png', 'agua.png', 'durmiendo.png', 'caminando.png', 'nada.png']
MODULOS_TOTALES = 5

def index(request):
	return render(request, 'index.html', {"MODULOS_TOTALES_LISTA":range(MODULOS_TOTALES), "MODULOS_TOTALES":MODULOS_TOTALES})
def mobile(request):
	return render(request, 'mobile.html', {'LISTA':zip(LISTA_ACTIVIDADES, LISTA_LINKS)})