from godot import exposed, export
from godot import *


@exposed
class TrafficLightArea(Node):
	vehicles_waiting1 = []
	vehicles_waiting2 = []
	vehicles_waiting3 = []
	vehicles_waiting4 = []
	vehicles_waiting5 = []
	vehicles_waiting6 = []
	vehicles_waiting7 = []
	vehicles_waiting8 = []
	vehicles_waiting9 = []
	vehicles_waiting10 = []
	vehicles_waiting11 = []
	vehicles_waiting12 = []
	vehicles_waiting13 = []
	vehicles_waiting14 = []
	vehicles_waiting15 = []
	vehicles_waiting16 = []
	vehicles_waiting17 = []
	vehicles_waiting18 = []
	vehicles_waiting19 = []
	vehicles_waiting20 = []
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
		if self.find_parent("World").find_node("trafficlight1").get_node("GreenLight").visible:
			for car in self.vehicles_waiting1:
				car.speed = car.normal_speed
			self.vehicles_waiting1.clear()
		if self.find_parent("World").find_node("trafficlight2").get_node("GreenLight").visible:
			for car in self.vehicles_waiting2:
				car.speed = car.normal_speed
			self.vehicles_waiting2.clear()
		if self.find_parent("World").find_node("trafficlight3").get_node("GreenLight").visible:
			for car in self.vehicles_waiting3:
				car.speed = car.normal_speed
			self.vehicles_waiting3.clear()
		if self.find_parent("World").find_node("trafficlight4").get_node("GreenLight").visible:
			for car in self.vehicles_waiting4:
				car.speed = car.normal_speed
			self.vehicles_waiting4.clear()
		if self.find_parent("World").find_node("trafficlight5").get_node("GreenLight").visible:
			for car in self.vehicles_waiting5:
				car.speed = car.normal_speed
			self.vehicles_waiting5.clear()
		if self.find_parent("World").find_node("trafficlight6").get_node("GreenLight").visible:
			for car in self.vehicles_waiting6:
				car.speed = car.normal_speed
			self.vehicles_waiting6.clear()
		if self.find_parent("World").find_node("trafficlight7").get_node("GreenLight").visible:
			for car in self.vehicles_waiting7:
				car.speed = car.normal_speed
			self.vehicles_waiting7.clear()
		if self.find_parent("World").find_node("trafficlight8").get_node("GreenLight").visible:
			for car in self.vehicles_waiting8:
				car.speed = car.normal_speed
			self.vehicles_waiting8.clear()
		if self.find_parent("World").find_node("trafficlight9").get_node("GreenLight").visible:
			for car in self.vehicles_waiting9:
				car.speed = car.normal_speed
			self.vehicles_waiting9.clear()
		if self.find_parent("World").find_node("trafficlight10").get_node("GreenLight").visible:
			for car in self.vehicles_waiting10:
				car.speed = car.normal_speed
			self.vehicles_waiting10.clear()
		if self.find_parent("World").find_node("trafficlight11").get_node("GreenLight").visible:
			for car in self.vehicles_waiting11:
				car.speed = car.normal_speed
			self.vehicles_waiting11.clear()
		if self.find_parent("World").find_node("trafficlight12").get_node("GreenLight").visible:
			for car in self.vehicles_waiting12:
				car.speed = car.normal_speed
			self.vehicles_waiting12.clear()
		if self.find_parent("World").find_node("trafficlight13").get_node("GreenLight").visible:
			for car in self.vehicles_waiting13:
				car.speed = car.normal_speed
			self.vehicles_waiting13.clear()
		if self.find_parent("World").find_node("trafficlight14").get_node("GreenLight").visible:
			for car in self.vehicles_waiting14:
				car.speed = car.normal_speed
			self.vehicles_waiting14.clear()
		if self.find_parent("World").find_node("trafficlight15").get_node("GreenLight").visible:
			for car in self.vehicles_waiting15:
				car.speed = car.normal_speed
			self.vehicles_waiting15.clear()
		if self.find_parent("World").find_node("trafficlight16").get_node("GreenLight").visible:
			for car in self.vehicles_waiting16:
				car.speed = car.normal_speed
			self.vehicles_waiting16.clear()
		if self.find_parent("World").find_node("trafficlight17").get_node("GreenLight").visible:
			for car in self.vehicles_waiting17:
				car.speed = car.normal_speed
			self.vehicles_waiting17.clear()
		if self.find_parent("World").find_node("trafficlight18").get_node("GreenLight").visible:
			for car in self.vehicles_waiting18:
				car.speed = car.normal_speed
			self.vehicles_waiting18.clear()
		if self.find_parent("World").find_node("trafficlight19").get_node("GreenLight").visible:
			for car in self.vehicles_waiting19:
				car.speed = car.normal_speed
			self.vehicles_waiting19.clear()
		if self.find_parent("World").find_node("trafficlight20").get_node("GreenLight").visible:
			for car in self.vehicles_waiting20:
				car.speed = car.normal_speed
			self.vehicles_waiting20.clear()
		if self.find_parent("World").find_node("trafficlight21a").get_node("GreenLight").visible:
			for car in self.vehicles_waiting21:
				car.speed = car.normal_speed
			self.vehicles_waiting21.clear()
		if self.find_parent("World").find_node("trafficlight22a").get_node("GreenLight").visible:
			for car in self.vehicles_waiting22:
				car.speed = car.normal_speed
			self.vehicles_waiting22.clear()
		if self.find_parent("World").find_node("trafficlight23a").get_node("GreenLight").visible:
			for car in self.vehicles_waiting23:
				car.speed = car.normal_speed
			self.vehicles_waiting23.clear()
		if self.find_parent("World").find_node("trafficlight24a").get_node("GreenLight").visible:
			for car in self.vehicles_waiting24:
				car.speed = car.normal_speed
			self.vehicles_waiting24.clear()
		if self.find_parent("World").find_node("trafficlight25a").get_node("GreenLight").visible:
			for car in self.vehicles_waiting25:
				car.speed = car.normal_speed
			self.vehicles_waiting25.clear()
		if self.find_parent("World").find_node("trafficlight26a").get_node("GreenLight").visible:
			for car in self.vehicles_waiting26:
				car.speed = car.normal_speed
			self.vehicles_waiting26.clear()
		if self.find_parent("World").find_node("trafficlight27a").get_node("GreenLight").visible:
			for car in self.vehicles_waiting27:
				car.speed = car.normal_speed
			self.vehicles_waiting27.clear()
		if self.find_parent("World").find_node("trafficlight28a").get_node("GreenLight").visible:
			for car in self.vehicles_waiting28:
				car.speed = car.normal_speed
			self.vehicles_waiting28.clear()
		if self.find_parent("World").find_node("trafficlight29a").get_node("GreenLight").visible:
			for car in self.vehicles_waiting29:
				car.speed = car.normal_speed
			self.vehicles_waiting29.clear()
		if self.find_parent("World").find_node("trafficlight30").get_node("GreenLight").visible:
			for car in self.vehicles_waiting30:
				car.speed = car.normal_speed
			self.vehicles_waiting30.clear()
		if self.find_parent("World").find_node("trafficlight31").get_node("GreenLight").visible:
			for car in self.vehicles_waiting31:
				car.speed = car.normal_speed
			self.vehicles_waiting31.clear()
		if self.find_parent("World").find_node("trafficlight32").get_node("GreenLight").visible:
			for car in self.vehicles_waiting32:
				car.speed = car.normal_speed
			self.vehicles_waiting32.clear()
		if self.find_parent("World").find_node("trafficlight33a").get_node("GreenLight").visible:
			for car in self.vehicles_waiting33:
				car.speed = car.normal_speed
			self.vehicles_waiting33.clear()
		if self.find_parent("World").find_node("trafficlight34a").get_node("GreenLight").visible:
			for car in self.vehicles_waiting34:
				car.speed = car.normal_speed
			self.vehicles_waiting34.clear()
		if self.find_parent("World").find_node("trafficlight35a").get_node("GreenLight").visible:
			for car in self.vehicles_waiting35:
				car.speed = car.normal_speed
			self.vehicles_waiting35.clear()
		pass
	
	def _on_TrafficLightArea1_body_entered(self, body):
		car = body.get_parent()
		greenlight = self.find_parent("World").find_node("trafficlight1").get_node("GreenLight").visible
		
		if greenlight != True:
			car.speed = 0
			self.vehicles_waiting1.append(car)
	
	def _on_TrafficLightArea2_body_entered(self, body):
		car = body.get_parent()
		greenlight = self.find_parent("World").find_node("trafficlight2").get_node("GreenLight").visible
		
		if greenlight != True:
			car.speed = 0
			self.vehicles_waiting2.append(car)
	
	def _on_TrafficLightArea3_body_entered(self, body):
		car = body.get_parent()
		greenlight = self.find_parent("World").find_node("trafficlight3").get_node("GreenLight").visible
		
		if greenlight != True:
			car.speed = 0
			self.vehicles_waiting3.append(car)
	
	def _on_TrafficLightArea4_body_entered(self, body):
		car = body.get_parent()
		greenlight = self.find_parent("World").find_node("trafficlight4").get_node("GreenLight").visible
		
		if greenlight != True:
			car.speed = 0
			self.vehicles_waiting4.append(car)
	
	def _on_TrafficLightArea5_body_entered(self, body):
		car = body.get_parent()
		greenlight = self.find_parent("World").find_node("trafficlight5").get_node("GreenLight").visible
		
		if greenlight != True:
			car.speed = 0
			self.vehicles_waiting5.append(car)
	
	def _on_TrafficLightArea6_body_entered(self, body):
		car = body.get_parent()
		greenlight = self.find_parent("World").find_node("trafficlight6").get_node("GreenLight").visible
		
		if greenlight != True:
			car.speed = 0
			self.vehicles_waiting6.append(car)
	
	def _on_TrafficLightArea7_body_entered(self, body):
		car = body.get_parent()
		greenlight = self.find_parent("World").find_node("trafficlight7").get_node("GreenLight").visible
		
		if greenlight != True:
			car.speed = 0
			self.vehicles_waiting7.append(car)
	
	def _on_TrafficLightArea8_body_entered(self, body):
		car = body.get_parent()
		greenlight = self.find_parent("World").find_node("trafficlight8").get_node("GreenLight").visible
		
		if greenlight != True:
			car.speed = 0
			self.vehicles_waiting8.append(car)
	
	def _on_TrafficLightArea9_body_entered(self, body):
		car = body.get_parent()
		greenlight = self.find_parent("World").find_node("trafficlight9").get_node("GreenLight").visible
		
		if greenlight != True:
			car.speed = 0
			self.vehicles_waiting9.append(car)
	
	def _on_TrafficLightArea10_body_entered(self, body):
		car = body.get_parent()
		greenlight = self.find_parent("World").find_node("trafficlight10").get_node("GreenLight").visible
		
		if greenlight != True:
			car.speed = 0
			self.vehicles_waiting10.append(car)
	
	def _on_TrafficLightArea11_body_entered(self, body):
		car = body.get_parent()
		greenlight = self.find_parent("World").find_node("trafficlight11").get_node("GreenLight").visible
		
		if greenlight != True:
			car.speed = 0
			self.vehicles_waiting11.append(car)
	
	def _on_TrafficLightArea12_body_entered(self, body):
		car = body.get_parent()
		greenlight = self.find_parent("World").find_node("trafficlight12").get_node("GreenLight").visible
		
		if greenlight != True:
			car.speed = 0
			self.vehicles_waiting12.append(car)
	
	def _on_TrafficLightArea13_body_entered(self, body):
		car = body.get_parent()
		greenlight = self.find_parent("World").find_node("trafficlight13").get_node("GreenLight").visible
		
		if greenlight != True:
			car.speed = 0
			self.vehicles_waiting13.append(car)
	
	def _on_TrafficLightArea14_body_entered(self, body):
		car = body.get_parent()
		greenlight = self.find_parent("World").find_node("trafficlight14").get_node("GreenLight").visible
		
		if greenlight != True:
			car.speed = 0
			self.vehicles_waiting14.append(car)
	
	def _on_TrafficLightArea15_body_entered(self, body):
		car = body.get_parent()
		greenlight = self.find_parent("World").find_node("trafficlight15").get_node("GreenLight").visible
		
		if greenlight != True:
			car.speed = 0
			self.vehicles_waiting15.append(car)
	
	def _on_TrafficLightArea16_body_entered(self, body):
		car = body.get_parent()
		greenlight = self.find_parent("World").find_node("trafficlight16").get_node("GreenLight").visible
		
		if greenlight != True:
			car.speed = 0
			self.vehicles_waiting16.append(car)
	
	def _on_TrafficLightArea17_body_entered(self, body):
		car = body.get_parent()
		greenlight = self.find_parent("World").find_node("trafficlight17").get_node("GreenLight").visible
		
		if greenlight != True:
			car.speed = 0
			self.vehicles_waiting17.append(car)
	
	def _on_TrafficLightArea18_body_entered(self, body):
		car = body.get_parent()
		greenlight = self.find_parent("World").find_node("trafficlight18").get_node("GreenLight").visible
		
		if greenlight != True:
			car.speed = 0
			self.vehicles_waiting18.append(car)
	
	def _on_TrafficLightArea19_body_entered(self, body):
		car = body.get_parent()
		greenlight = self.find_parent("World").find_node("trafficlight19").get_node("GreenLight").visible
		
		if greenlight != True:
			car.speed = 0
			self.vehicles_waiting19.append(car)
	
	def _on_TrafficLightArea20_body_entered(self, body):
		car = body.get_parent()
		greenlight = self.find_parent("World").find_node("trafficlight20").get_node("GreenLight").visible
		
		if greenlight != True:
			car.speed = 0
			self.vehicles_waiting20.append(car)
	
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
