from godot import exposed, export
from godot import *


@exposed
class bridge(Spatial):

	# member variables here, example:
	#a = export(int)
	#b = export(str, default='foo')
	
	up = Vector3(-90, 0, 0)
	down = Vector3(0, 0, 0)
	
	time_passed=0
	going_up=export(bool, default=True)
	rotation_speed=0.1
	

	def _ready(self):
		#self.set_rotation_degrees(self.rotated)
		pass
	
	def _process(self, delta):
		self.time_passed += delta
		if self.going_up and self.rotation_degrees.x > -89.5:
			self.set_rotation_degrees(self.down.linear_interpolate(self.up, self.time_passed * self.rotation_speed))
		elif not self.going_up and self.rotation_degrees.x < -0.1:
			self.set_rotation_degrees(self.up.linear_interpolate(self.down, self.time_passed * self.rotation_speed))
		else:
			self.time_passed = 0
			self.going_up = False
