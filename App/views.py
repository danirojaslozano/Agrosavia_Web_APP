from django.shortcuts import render,redirect,render_to_response
from django.http import HttpResponse
from django.http import Http404
import simplejson as json
import time
import socket
import threading
import pyexcel
import django_excel as excel
import numpy as np

global LISTA_ACTIVIDADES, LISTA_LINKS, ACTIVIDAD_ACTUAL

LISTA_ACTIVIDADES = ['Comiendo(Elíptica)', 'Rumiando(Trotadora)', 'Tomando Agua(Escaladora)', 'Durmiendo', 'Caminando', 'Nada']

LISTA_LINKS = ['comiendo.png', 'rumia.png', 'agua.png', 'durmiendo.png', 'caminando.png', 'nada.png']

ACTIVIDAD_ACTUAL = [5, 5, 5, 5, 5] # Variables para la acividad de los 5 nodos (clientes)

global tiempoInicio
tiempoInicio = time.time() #Variable que guarda el tiempo en el que el servidor empezó a correr

global fechaYhora
fechaYhora = "" #Variable para etiquetar los datos con fechas y horas

global Vacio
Vacio = [] #Variable para dar organización al archivo excel. No tiene ningún otro uso

global Nada
Nada = "    " #Variable para dar organización al archivo plano de texto. No tiene ningun otro uso

global datos
datos = [0, 0, 0, 0, 0, 0, 0, 0] # Acc_x, Acc_y, Acc_z, Gyro_x, Gyro_y , Gyro_z, Acc_Id, Acc_Num

global vacas, vaca1, vaca2, vaca3
vaca1 = [[],[],[],[],[],[],[],[],[],[],[]] # AcumAccX1, AcumAccY1, AcumAccZ1, AcumGyroX1, AcumGyroY1, AcumGyroZ1, AcumActividad1, AcumId1, AcumNum1, AcumTiempo1, AcumTiempoF1
vaca2 = [[],[],[],[],[],[],[],[],[],[],[]]
vaca3 = [[],[],[],[],[],[],[],[],[],[],[]]
vacas = [[], [], []]

lock = threading.Lock()

global cnx_accel1, cnx_accel2, cnx_accel3
cnx_accel1 = False
cnx_accel2 = False
cnx_accel3 = False

### IP del computador servidor
global UDP_IP
UDP_IP = "192.168.0.102"


def ThreadActualizarSocket():
	global datos, vacas, vaca1, vaca2, vaca3, fechaYhora, cnx_accel1, cnx_accel2, cnx_accel3

	UDP_PORT = 9001 ## Este puerto debe coincidir con el configurado en el módulo wifi para el envío de datos

	s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
	s.bind((UDP_IP, UDP_PORT))

	while True:

		data, addr = s.recvfrom(1024)
		data = data.decode()

		file = open("datosAccel","a") #Se activa (crea) el archivo para guardar (escribir) un nuevo dato

		try:

			ArrayData = data.split("#")

			datos[0] = float(ArrayData[0])
			datos[1] = float(ArrayData[1])
			datos[2] = float(ArrayData[2])
			datos[3] = float(ArrayData[3])
			datos[4] = float(ArrayData[4])
			datos[5] = float(ArrayData[5])
			datos[6] = float(ArrayData[6])
			datos[7] = float(ArrayData[7])

			fechaYhora = str(time.strftime("%c"))

			lock.acquire()

			if datos[6]==1:
				vaca1[0].append(datos[0])
				vaca1[1].append(datos[1])
				vaca1[2].append(datos[2])
				vaca1[3].append(datos[3])
				vaca1[4].append(datos[4])
				vaca1[5].append(datos[5])
				vaca1[6].append(datos[6])
				vaca1[7].append(datos[7])
				vaca1[8].append(LISTA_ACTIVIDADES[ACTIVIDAD_ACTUAL[0]])
				vaca1[9].append(time.time()-tiempoInicio)
				vaca1[10].append(fechaYhora)
				cnx_accel1 = True

			elif datos[6]==2:
				vaca2[0].append(datos[0])
				vaca2[1].append(datos[1])
				vaca2[2].append(datos[2])
				vaca2[3].append(datos[3])
				vaca2[4].append(datos[4])
				vaca2[5].append(datos[5])
				vaca2[6].append(datos[6])
				vaca2[7].append(datos[7])
				vaca2[8].append(LISTA_ACTIVIDADES[ACTIVIDAD_ACTUAL[1]])
				vaca2[9].append(time.time()-tiempoInicio)
				vaca2[10].append(fechaYhora)
				cnx_accel2 = True

			elif datos[6]==3:
				vaca3[0].append(datos[0])
				vaca3[1].append(datos[1])
				vaca3[2].append(datos[2])
				vaca3[3].append(datos[3])
				vaca3[4].append(datos[4])
				vaca3[5].append(datos[5])
				vaca3[6].append(datos[6])
				vaca3[7].append(datos[7])
				vaca3[8].append(LISTA_ACTIVIDADES[ACTIVIDAD_ACTUAL[0]])
				vaca3[9].append(time.time()-tiempoInicio)
				vaca3[10].append(fechaYhora)
				cnx_accel3 = True

			else:
				print("Dato de un cliente no aceptado")

			lock.release()

			file.write( ("%.10f \t %.10f \t %.10f \t %.10f \t %.10f \t %.10f \t %.10f \t %.10f \t %.10f \t"%(time.time()-tiempoInicio, datos[7], datos[6], datos[0], datos[1], datos[2], datos[3], datos[4], datos[5]) ) + Nada + LISTA_ACTIVIDADES[ACTIVIDAD_ACTUAL[0]] + Nada + LISTA_ACTIVIDADES[ACTIVIDAD_ACTUAL[1]] + Nada + LISTA_ACTIVIDADES[ACTIVIDAD_ACTUAL[2]] + "\n" )

			file.close() #Cada vez que el servidor recibe un dato lo guarda adecuamente en el archivo plano de texto
					  	 #para evitar perdidas de datos

		except:
			print("Error en dato")


threading.Thread(target=ThreadActualizarSocket).start()


## Estas son las funciones para cada uno de los modulos, para seleccionar independientemente la actidad actual de cada cliente (5 en total)
def index1(request):

	global LISTA_ACTIVIDADES

	return render(request, 'index1.html', {'LISTA':zip(LISTA_ACTIVIDADES, LISTA_LINKS), 'ACTUAL':ACTIVIDAD_ACTUAL[0]})

def actualizar_estado1(request):

	global ACTIVIDAD_ACTUAL

	ACTIVIDAD_ACTUAL[0] = int(request.POST['estado'])

	return HttpResponse(str(ACTIVIDAD_ACTUAL[0]))


def index2(request):

	global LISTA_ACTIVIDADES

	return render(request, 'index2.html', {'LISTA':zip(LISTA_ACTIVIDADES, LISTA_LINKS), 'ACTUAL':ACTIVIDAD_ACTUAL[1]})

def actualizar_estado2(request):

	global ACTIVIDAD_ACTUAL

	ACTIVIDAD_ACTUAL[1] = int(request.POST['estado'])

	return HttpResponse(str(ACTIVIDAD_ACTUAL[1]))


def index3(request):

	global LISTA_ACTIVIDADES

	return render(request, 'index3.html', {'LISTA':zip(LISTA_ACTIVIDADES, LISTA_LINKS), 'ACTUAL':ACTIVIDAD_ACTUAL[2]})

def actualizar_estado3(request):

	global ACTIVIDAD_ACTUAL

	ACTIVIDAD_ACTUAL[2] = int(request.POST['estado'])

	return HttpResponse(str(ACTIVIDAD_ACTUAL[2]))


def index4(request):

	global LISTA_ACTIVIDADES

	return render(request, 'index4.html', {'LISTA':zip(LISTA_ACTIVIDADES, LISTA_LINKS), 'ACTUAL':ACTIVIDAD_ACTUAL[3]})

def actualizar_estado4(request):

	global ACTIVIDAD_ACTUAL

	ACTIVIDAD_ACTUAL[3] = int(request.POST['estado'])

	return HttpResponse(str(ACTIVIDAD_ACTUAL[3]))


def index5(request):

	global LISTA_ACTIVIDADES

	return render(request, 'index5.html', {'LISTA':zip(LISTA_ACTIVIDADES, LISTA_LINKS), 'ACTUAL':ACTIVIDAD_ACTUAL[4]})

def actualizar_estado5(request):

	global ACTIVIDAD_ACTUAL

	ACTIVIDAD_ACTUAL[4] = int(request.POST['estado'])

	return HttpResponse(str(ACTIVIDAD_ACTUAL[4]))


## La actualización de la actividad en el servidor se realiza con los datos del primer modulo (cliente 1), pero los datos de todos los demás módulos
## se están guardando igualmente.
def server(request):

	global ACTIVIDAD_ACTUAL, LISTA_ACTIVIDADES, LISTA_LINKS

	return render(request, 'server.html', {'Actividad':LISTA_ACTIVIDADES[ACTIVIDAD_ACTUAL[0]], 'Imagen': LISTA_LINKS[ACTIVIDAD_ACTUAL[0]], 'Actividad2':LISTA_ACTIVIDADES[ACTIVIDAD_ACTUAL[1]], 'Imagen2': LISTA_LINKS[ACTIVIDAD_ACTUAL[1]], 'Actividad3':LISTA_ACTIVIDADES[ACTIVIDAD_ACTUAL[2]], 'Imagen3': LISTA_LINKS[ACTIVIDAD_ACTUAL[2]]})


def actualizarServer(request):

	global ACTIVIDAD_ACTUAL, LISTA_ACTIVIDADES, LISTA_LINKS, datos, vacas, vaca1, vaca2, vaca3, tiempoInicio, cnx_accel1, cnx_accel2, cnx_accel3

	if vaca1[9] and (np.abs(time.time()-tiempoInicio - vaca1[9][-1]) > 2):
		cnx_accel1 = False
	if vaca2[9] and (np.abs(time.time()-tiempoInicio - vaca2[9][-1]) > 2):
		cnx_accel2 = False
	if vaca3[9] and (np.abs(time.time()-tiempoInicio - vaca3[9][-1]) > 2):
		cnx_accel3 = False

	respuesta = {}

	respuesta['texto'] = LISTA_ACTIVIDADES[ACTIVIDAD_ACTUAL[0]]
	respuesta['imagen'] = LISTA_LINKS[ACTIVIDAD_ACTUAL[0]]
	respuesta['texto2'] = LISTA_ACTIVIDADES[ACTIVIDAD_ACTUAL[1]]
	respuesta['imagen2'] = LISTA_LINKS[ACTIVIDAD_ACTUAL[1]]
	respuesta['texto3'] = LISTA_ACTIVIDADES[ACTIVIDAD_ACTUAL[2]]
	respuesta['imagen3'] = LISTA_LINKS[ACTIVIDAD_ACTUAL[2]]

	if (datos[6] == 1):
		respuesta['Acc_x'] = datos[0]
		respuesta['Acc_y'] = datos[1]
		respuesta['Acc_z'] = datos[2]
		respuesta['Gyro_x'] = datos[3]
		respuesta['Gyro_y'] = datos[4]
		respuesta['Gyro_z'] = datos[5]
		respuesta['tiempo'] = time.time()-tiempoInicio

	elif (datos[6] == 2):
		respuesta['Acc_x2'] = datos[0]
		respuesta['Acc_y2'] = datos[1]
		respuesta['Acc_z2'] = datos[2]
		respuesta['Gyro_x2'] = datos[3]
		respuesta['Gyro_y2'] = datos[4]
		respuesta['Gyro_z2'] = datos[5]
		respuesta['tiempo2'] = time.time()-tiempoInicio

	elif (datos[6] == 3):
		respuesta['Acc_x3'] = datos[0]
		respuesta['Acc_y3'] = datos[1]
		respuesta['Acc_z3'] = datos[2]
		respuesta['Gyro_x3'] = datos[3]
		respuesta['Gyro_y3'] = datos[4]
		respuesta['Gyro_z3'] = datos[5]
		respuesta['tiempo3'] = time.time()-tiempoInicio

	respuesta['estadoAccel1'] = cnx_accel1
	respuesta['estadoAccel2'] = cnx_accel2
	respuesta['estadoAccel3'] = cnx_accel3

	datos[6] = 0; #Para que el servidor deje de pintar datos cuandos los modulos están desconectados

	return HttpResponse(json.dumps(respuesta))


def exportarDatosExcel(request): ##Se exportan los datos a un archivo de excel organizado

	lock.acquire()
	sheet = pyexcel.get_sheet(array = [vaca1[10], vaca1[6], vaca1[7], vaca1[0], vaca1[1], vaca1[2], vaca1[3], vaca1[4], vaca1[5], vaca1[8], Vacio, vaca2[10], vaca2[6], vaca2[7], vaca2[0], vaca2[1], vaca2[2], vaca2[3], vaca2[4], vaca2[5], vaca2[8], Vacio, vaca3[10], vaca3[6], vaca3[7], vaca3[0], vaca3[1], vaca3[2], vaca3[3], vaca3[4], vaca3[5], vaca3[8]])
	lock.release()

	sheet.transpose()

	return excel.make_response(sheet, "xlsx")
