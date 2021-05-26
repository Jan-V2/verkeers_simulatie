from godot import exposed, export
from godot import *


@exposed
class bridge(Spatial):
	#Class variables
	going_up=export(bool, default=False)
	up = Vector3(-90, 0, 0)
	down = Vector3(0, 0, 0)
	rotation_speed=0.2
	time_passed=0
	epoch_time=0
	
	#Goes up or down according to going_up attribute
	def _process(self, delta):
		self.time_passed += delta
		self.epoch_time += delta
		if self.going_up and self.rotation_degrees.x > -89.5:
			self.set_rotation_degrees(self.down.linear_interpolate(self.up, self.time_passed * self.rotation_speed))
		elif not self.going_up and self.rotation_degrees.x < -0.1:
			self.set_rotation_degrees(self.up.linear_interpolate(self.down, self.time_passed * self.rotation_speed))
		else:
			self.time_passed = 0
			
		#Controls the warning lights
		warning_lights_state = not self.rotation_degrees.x > -0.1 and round(self.epoch_time) % 2 == 0
		self.find_parent("Intersection").find_node("alarmlightcomplete1").find_node("OrangeLight").visible = warning_lights_state
		self.find_parent("Intersection").find_node("alarmlightcomplete2").find_node("OrangeLight").visible = warning_lights_state
		self.find_parent("Intersection").find_node("alarmlightcomplete3").find_node("OrangeLight").visible = warning_lights_state
		self.find_parent("Intersection").find_node("alarmlightcomplete4").find_node("OrangeLight").visible = warning_lights_state
		self.find_parent("Intersection").find_node("alarmlightcomplete5").find_node("OrangeLight").visible = warning_lights_state
		self.find_parent("Intersection").find_node("alarmlightcomplete6").find_node("OrangeLight").visible = warning_lights_state
