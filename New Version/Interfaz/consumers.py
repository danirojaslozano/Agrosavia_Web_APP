from asgiref.sync import async_to_sync
from channels.generic.websocket import WebsocketConsumer
import channels.layers
import simplejson as json
import time
import threading
import numpy as np
channel_layer = channels.layers.get_channel_layer()

LISTA_ACTIVIDADES = ['Comiendo', 'Rumiando', 'Tomando Agua', 'Durmiendo', 'Caminando', 'Nada']
LISTA_LINKS = ['comiendo.png', 'rumia.png', 'agua.png', 'durmiendo.png', 'caminando.png', 'nada.png']
MODULOS_TOTALES = 5

global connectionStatus, currentActivity, startTime
connectionStatus = [1,1,0,0,1] #np.zeros(MODULOS_TOTALES)
currentActivity = 5 * np.ones(MODULOS_TOTALES)
startTime = time.time()

class bgUpdate(WebsocketConsumer):
	def connect(self):
		self.room_name = 'r'+str(time.time())
		self.room_group_name = 'bgUpdateConsumers'

		# Join room group
		async_to_sync(self.channel_layer.group_add)(
			self.room_group_name,
			self.channel_name
		)
		self.accept()

	def disconnect(self, close_code):
		async_to_sync(self.channel_layer.group_discard)(
			self.room_group_name,
			self.channel_name
		)

	def receive(self, text_data):

		text_data_json = json.loads(text_data)

	def updateGUI(self, event):

		self.send(text_data=json.dumps(event))

def threadGUIupdate():

	global connectionStatus

	while True:

		options = {}
		options['type'] = 'updateGUI'

		options['ConnectionStatus'] = list(connectionStatus)

		async_to_sync(channel_layer.group_send)('bgUpdateConsumers', options)

		time.sleep(100E-3)

	
threading.Thread(target=threadGUIupdate).start()



