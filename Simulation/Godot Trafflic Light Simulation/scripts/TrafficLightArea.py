from godot import exposed, export
from godot import *


@exposed
class TrafficLightArea(Node):
	vehicles_waiting21 = []
	vehicles_waiting22 = []
	vehicles_waiting23 = []
	vehicles_waiting24 = []
	vehicles_waiting25 = []
	vehicles_waiting26 = []
	vehicles_waiting27 = []
	vehicles_waiting28 = []
	vehicles_waiting29 = []
	vehicles_waiting30 = []
	vehicles_waiting31 = []
	vehicles_waiting32 = []
	vehicles_waiting33 = []
	vehicles_waiting34 = []
	vehicles_waiting35 = []

	def _ready(self):
		"""
		Called every time the node is added to the scene.
		Initialization here.
		"""
		pass
		
	def _process(self, delta):
		if self.find_parent("World").find_node("trafficlight21a").get_node("GreenLight").visible:
			for car in self.vehicles_waiting21:
				car.speed = 10
			self.vehicles_waiting21.clear()
		if self.find_parent("World").find_node("trafficlight22a").get_node("GreenLight").visible:
			for car in self.vehicles_waiting22:
				car.speed = 10
			self.vehicles_waiting22.clear()
		if self.find_parent("World").find_node("trafficlight23a").get_node("GreenLight").visible:
			for car in self.vehicles_waiting23:
				car.speed = 10
			self.vehicles_waiting23.clear()
		if self.find_parent("World").find_node("trafficlight24a").get_node("GreenLight").visible:
			for car in self.vehicles_waiting24:
				car.speed = 10
			self.vehicles_waiting24.clear()
		if self.find_parent("World").find_node("trafficlight25a").get_node("GreenLight").visible:
			for car in self.vehicles_waiting25:
				car.speed = 10
			self.vehicles_waiting25.clear()
		if self.find_parent("World").find_node("trafficlight26a").get_node("GreenLight").visible:
			for car in self.vehicles_waiting26:
				car.speed = 10
			self.vehicles_waiting26.clear()
		if self.find_parent("World").find_node("trafficlight27a").get_node("GreenLight").visible:
			for car in self.vehicles_waiting27:
				car.speed = 10
			self.vehicles_waiting27.clear()
		if self.find_parent("World").find_node("trafficlight28a").get_node("GreenLight").visible:
			for car in self.vehicles_waiting28:
				car.speed = 10
			self.vehicles_waiting28.clear()
		if self.find_parent("World").find_node("trafficlight29a").get_node("GreenLight").visible:
			for car in self.vehicles_waiting29:
				car.speed = 10
			self.vehicles_waiting29.clear()
		if self.find_parent("World").find_node("trafficlight30").get_node("GreenLight").visible:
			for car in self.vehicles_waiting30:
				car.speed = 10
			self.vehicles_waiting30.clear()
		if self.find_parent("World").find_node("trafficlight31").get_node("GreenLight").visible:
			for car in self.vehicles_waiting31:
				car.speed = 10
			self.vehicles_waiting31.clear()
		if self.find_parent("World").find_node("trafficlight32").get_node("GreenLight").visible:
			for car in self.vehicles_waiting32:
				car.speed = 10
			self.vehicles_waiting32.clear()
		if self.find_parent("World").find_node("trafficlight33a").get_node("GreenLight").visible:
			for car in self.vehicles_waiting33:
				car.speed = 10
			self.vehicles_waiting33.clear()
		if self.find_parent("World").find_node("trafficlight34a").get_node("GreenLight").visible:
			for car in self.vehicles_waiting34:
				car.speed = 10
			self.vehicles_waiting34.clear()
		if self.find_parent("World").find_node("trafficlight35a").get_node("GreenLight").visible:
			for car in self.vehicles_waiting35:
				car.speed = 10
			self.vehicles_waiting35.clear()
		pass
	
	def _on_TrafficLightArea21_body_entered(self, body):
		car = body.get_parent()
		greenlight = self.find_parent("World").find_node("trafficlight21a").get_node("GreenLight").visible
		
		if greenlight != True:
			car.speed = 0
			self.vehicles_waiting21.append(car)
	
	def _on_TrafficLightArea22_body_entered(self, body):
		car = body.get_parent()
		greenlight = self.find_parent("World").find_node("trafficlight22a").get_node("GreenLight").visible
		
		if greenlight != True:
			car.speed = 0
			self.vehicles_waiting22.append(car)
	
	def _on_TrafficLightArea23_body_entered(self, body):
		car = body.get_parent()
		greenlight = self.find_parent("World").find_node("trafficlight23a").get_node("GreenLight").visible
		
		if greenlight != True:
			car.speed = 0
			self.vehicles_waiting23.append(car)
	
	def _on_TrafficLightArea24_body_entered(self, body):
		car = body.get_parent()
		greenlight = self.find_parent("World").find_node("trafficlight24a").get_node("GreenLight").visible
		
		if greenlight != True:
			car.speed = 0
			self.vehicles_waiting24.append(car)
	
	def _on_TrafficLightArea25_body_entered(self, body):
		car = body.get_parent()
		greenlight = self.find_parent("World").find_node("trafficlight25a").get_node("GreenLight").visible
		
		if greenlight != True:
			car.speed = 0
			self.vehicles_waiting25.append(car)
				
	def _on_TrafficLightArea26_body_entered(self, body):
		car = body.get_parent()
		greenlight = self.find_parent("World").find_node("trafficlight26a").get_node("GreenLight").visible
		
		if greenlight != True:
			car.speed = 0
			self.vehicles_waiting26.append(car)
	
	def _on_TrafficLightArea27_body_entered(self, body):
		car = body.get_parent()
		greenlight = self.find_parent("World").find_node("trafficlight27a").get_node("GreenLight").visible
		
		if greenlight != True:
			car.speed = 0
			self.vehicles_waiting27.append(car)
	
	def _on_TrafficLightArea28_body_entered(self, body):
		car = body.get_parent()
		greenlight = self.find_parent("World").find_node("trafficlight28a").get_node("GreenLight").visible
		
		if greenlight != True:
			car.speed = 0
			self.vehicles_waiting28.append(car)
	
	def _on_TrafficLightArea29_body_entered(self, body):
		car = body.get_parent()
		greenlight = self.find_parent("World").find_node("trafficlight29a").get_node("GreenLight").visible
		
		if greenlight != True:
			car.speed = 0
			self.vehicles_waiting29.append(car)
	
	def _on_TrafficLightArea30_body_entered(self, body):
		car = body.get_parent()
		greenlight = self.find_parent("World").find_node("trafficlight30").get_node("GreenLight").visible
		
		if greenlight != True:
			car.speed = 0
			self.vehicles_waiting30.append(car)
	
	def _on_TrafficLightArea31_body_entered(self, body):
		car = body.get_parent()
		greenlight = self.find_parent("World").find_node("trafficlight31").get_node("GreenLight").visible
		
		if greenlight != True:
			car.speed = 0
			self.vehicles_waiting31.append(car)
	
	def _on_TrafficLightArea32_body_entered(self, body):
		car = body.get_parent()
		greenlight = self.find_parent("World").find_node("trafficlight32").get_node("GreenLight").visible
		
		if greenlight != True:
			car.speed = 0
			self.vehicles_waiting32.append(car)
	
	def _on_TrafficLightArea33_body_entered(self, body):
		car = body.get_parent()
		greenlight = self.find_parent("World").find_node("trafficlight33a").get_node("GreenLight").visible
		
		if greenlight != True:
			car.speed = 0
			self.vehicles_waiting33.append(car)
	
	def _on_TrafficLightArea34_body_entered(self, body):
		car = body.get_parent()
		greenlight = self.find_parent("World").find_node("trafficlight34a").get_node("GreenLight").visible
		
		if greenlight != True:
			car.speed = 0
			self.vehicles_waiting34.append(car)
	
	def _on_TrafficLightArea35_body_entered(self, body):
		car = body.get_parent()
		greenlight = self.find_parent("World").find_node("trafficlight35a").get_node("GreenLight").visible
		
		if greenlight != True:
			car.speed = 0
			self.vehicles_waiting35.append(car)
