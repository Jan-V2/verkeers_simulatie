from godot import exposed, export
from godot import *

@exposed
class TLA(Node):
	#Just one class variable this time
	traffic_light = export(str, default='foo')
	
	def _ready(self):
		#This keeps track of waiting entities, has to be declared here or else it becomes a static variable?!
		self.vehicles_waiting = []

	def _process(self, delta):
		#Checks if waiting vehicles can move again
		if self.find_parent("World").find_node(self.traffic_light).get_node("GreenLight").visible:
			for car in self.vehicles_waiting:
				car.speed = car.normal_speed
			self.vehicles_waiting.clear()

	def _on_TrafficLightArea_body_entered(self, body):
		#Halts vehicles for red lights
		car = body.get_parent()
		if not self.find_parent("World").find_node(self.traffic_light).get_node("GreenLight").visible:
			car.speed = 0
			self.vehicles_waiting.append(car)
