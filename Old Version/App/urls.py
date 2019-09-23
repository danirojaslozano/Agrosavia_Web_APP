from django.urls import path
from django.urls import include, re_path
from django.views.generic.base import RedirectView

favicon_view = RedirectView.as_view(url='/static/favicon.png', permanent=True)

from . import views

urlpatterns = [
	path('favicon.ico', favicon_view, name='favicon'),
	path('', views.server, name='server'),
	path('actualizarServer', views.actualizarServer, name='actualizarServer'),
	path('exportarDatosExcel.xlsx', views.exportarDatosExcel, name='exportarDatosExcel'),
	path('1', views.index1, name='index1'),
	path('actualizar_estado1', views.actualizar_estado1, name='actualizar_estado1'),
	path('2', views.index2, name='index2'),
	path('actualizar_estado2', views.actualizar_estado2, name='actualizar_estado2'),
	path('3', views.index3, name='index3'),
	path('actualizar_estado3', views.actualizar_estado3, name='actualizar_estado3'),
	path('4', views.index4, name='index4'),
	path('actualizar_estado4', views.actualizar_estado4, name='actualizar_estado4'),
	path('5', views.index5, name='index5'),
	path('actualizar_estado5', views.actualizar_estado5, name='actualizar_estado5')
]
