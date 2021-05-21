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
		vehicles_waiting21 = []
		car = body.get_parent()
		greenlight = self.find_parent("World").find_node("trafficlight21a").get_node("GreenLight").visible
		
		if greenlight != True:
			car.speed = 0
			vehicles_waiting21.append(car)
		else:
			for vehicle in vehicles_waiting21:
				vehicle.speed = 10
				vehicles_waiting21.clear()
	
	def _on_TrafficLightArea22_body_entered(self, body):
		vehicles_waiting22 = []
		car = body.get_parent()
		greenlight = self.find_parent("World").find_node("trafficlight22a").get_node("GreenLight").visible
		
		if greenlight != True:
			car.speed = 0
			vehicles_waiting22.append(car)
		else:
			for vehicle in vehicles_waiting22:
				vehicle.speed = 10
				vehicles_waiting22.clear()
	
	def _on_TrafficLightArea23_body_entered(self, body):
		vehicles_waiting23 = []
		car = body.get_parent()
		greenlight = self.find_parent("World").find_node("trafficlight23a").get_node("GreenLight").visible
		
		if greenlight != True:
			car.speed = 0
			vehicles_waiting23.append(car)
		else:
			for vehicle in vehicles_waiting23:
				vehicle.speed = 10
				vehicles_waiting23.clear()
	
	def _on_TrafficLightArea24_body_entered(self, body):
		vehicles_waiting24 = []
		car = body.get_parent()
		greenlight = self.find_parent("World").find_node("trafficlight24a").get_node("GreenLight").visible
		
		if greenlight != True:
			car.speed = 0
			vehicles_waiting24.append(car)
		else:
			for vehicle in vehicles_waiting24:
				vehicle.speed = 10
				vehicles_waiting24.clear()
	
	def _on_TrafficLightArea25_body_entered(self, body):
		vehicles_waiting25 = []
		car = body.get_parent()
		greenlight = self.find_parent("World").find_node("trafficlight25a").get_node("GreenLight").visible
		
		if greenlight != True:
			car.speed = 0
			vehicles_waiting25.append(car)
		else:
			for vehicle in vehicles_waiting25:
				vehicle.speed = 10
				vehicles_waiting25.clear()
				
	def _on_TrafficLightArea26_body_entered(self, body):
		vehicles_waiting26 = []
		car = body.get_parent()
		greenlight = self.find_parent("World").find_node("trafficlight26a").get_node("GreenLight").visible
		
		if greenlight != True:
			car.speed = 0
			vehicles_waiting26.append(car)
		else:
			for vehicle in vehicles_waiting26:
				vehicle.speed = 10
				vehicles_waiting26.clear()
	
	def _on_TrafficLightArea27_body_entered(self, body):
		vehicles_waiting27 = []
		car = body.get_parent()
		greenlight = self.find_parent("World").find_node("trafficlight27a").get_node("GreenLight").visible
		
		if greenlight != True:
			car.speed = 0
			vehicles_waiting27.append(car)
		else:
			for vehicle in vehicles_waiting27:
				vehicle.speed = 10
				vehicles_waiting27.clear()
	
	def _on_TrafficLightArea28_body_entered(self, body):
		vehicles_waiting28 = []
		car = body.get_parent()
		greenlight = self.find_parent("World").find_node("trafficlight28a").get_node("GreenLight").visible
		
		if greenlight != True:
			car.speed = 0
			vehicles_waiting28.append(car)
		else:
			for vehicle in vehicles_waiting28:
				vehicle.speed = 10
				vehicles_waiting28.clear()
	
	def _on_TrafficLightArea29_body_entered(self, body):
		vehicles_waiting29 = []
		car = body.get_parent()
		greenlight = self.find_parent("World").find_node("trafficlight29a").get_node("GreenLight").visible
		
		if greenlight != True:
			car.speed = 0
			vehicles_waiting29.append(car)
		else:
			for vehicle in vehicles_waiting29:
				vehicle.speed = 10
				vehicles_waiting29.clear()
	
	def _on_TrafficLightArea30_body_entered(self, body):
		vehicles_waiting30 = []
		car = body.get_parent()
		greenlight = self.find_parent("World").find_node("trafficlight30").get_node("GreenLight").visible
		
		if greenlight != True:
			car.speed = 0
			vehicles_waiting30.append(car)
		else:
			for vehicle in vehicles_waiting30:
				vehicle.speed = 10
				vehicles_waiting30.clear()
	
	def _on_TrafficLightArea31_body_entered(self, body):
		vehicles_waiting31 = []
		car = body.get_parent()
		greenlight = self.find_parent("World").find_node("trafficlight31").get_node("GreenLight").visible
		
		if greenlight != True:
			car.speed = 0
			vehicles_waiting31.append(car)
		else:
			for vehicle in vehicles_waiting31:
				vehicle.speed = 10
				vehicles_waiting31.clear()
	
	def _on_TrafficLightArea32_body_entered(self, body):
		vehicles_waiting32 = []
		car = body.get_parent()
		greenlight = self.find_parent("World").find_node("trafficlight32").get_node("GreenLight").visible
		
		if greenlight != True:
			car.speed = 0
			vehicles_waiting32.append(car)
		else:
			for vehicle in vehicles_waiting32:
				vehicle.speed = 10
				vehicles_waiting32.clear()
