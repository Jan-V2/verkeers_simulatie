from godot import exposed, export
from godot import *


@exposed
class TrafficLightArea(Node):

	def _ready(self):
		"""
		Called every time the node is added to the scene.
		Initialization here.
		"""
		pass
	
	def _on_TrafficLightArea21_body_entered(self, body):
		#print('hoi')
		vehicles_waiting21 = []
		greenlight = self.find_parent("World").find_node("trafficlight21a").get_node("GreenLight").visible
		
		while greenlight != True:
			body.get_parent().speed = 0
			vehicles_waiting21.extend(body.get_parent())
		else:
			for vehicle in vehicles_waiting21:
				vehicle.speed = 10
				vehicles_waiting21.clear()
	
	#def _on_TrafficLightArea23_body_entered(self, body):
	
	#def _on_TrafficLightArea24_body_entered(self, body):
	
	#def _on_TrafficLightArea25_body_entered(self, body):
	
	#def _on_TrafficLightArea26_body_entered(self, body):
	
	#def _on_TrafficLightArea27_body_entered(self, body):
	
	#def _on_TrafficLightArea28_body_entered(self, body):
	
	#def _on_TrafficLightArea29_body_entered(self, body):
	
	#def _on_TrafficLightArea30_body_entered(self, body):
	
	#def _on_TrafficLightArea31_body_entered(self, body):
	
	#def _on_TrafficLightArea32_body_entered(self, body):
