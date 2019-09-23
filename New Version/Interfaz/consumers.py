from asgiref.sync import async_to_sync
from channels.generic.websocket import WebsocketConsumer
import channels.layers
import simplejson as json
import time
import threading
channel_layer = channels.layers.get_channel_layer()


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

def threadGUIupdate(node1_num, node2_num, node3_num, node4_num, node5_num, node6_num, op_node1_num, op_node2_num, op_node3_num, op_node4_num, op_node5_num, op_node6_num):

	options = {}
	options['type'] = 'updateGUI'

	async_to_sync(channel_layer.group_send)('bgUpdateConsumers', options)

	




