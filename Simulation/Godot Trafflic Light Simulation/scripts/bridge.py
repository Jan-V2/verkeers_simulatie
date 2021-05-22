from godot import exposed, export
from godot import *


@exposed
class bridge(Spatial):

	# member variables here, example:
	#a = export(int)
	#b = export(str, default='foo')
	
	b = Vector3(-90, 0, 0)
	a = Vector3(0, 0, 0)
	

	def _ready(self):
		#self.set_rotation_degrees(self.rotated)
		pass
	
	def _process(self, delta):
		rotation_speed = 0.2 * delta
		self.a = self.a.linear_interpolate(self.b, rotation_speed)
		print(self.a)
		#self.translation = self.translation.linear_interpolate(self.rotated, rotation_speed)
		self.set_rotation_degrees(self.a)
