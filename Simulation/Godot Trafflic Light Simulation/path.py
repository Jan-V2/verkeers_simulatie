from godot import exposed, export
from godot import *


@exposed
class path(Path):

	# member variables here, example:
	a = export(int)
	b = export(str, default='foo')

	def _ready(self):
		self.time_passed = 0
		
		pass
		
	def _process(self, delta):
		self.time_passed += delta
		if self.time_passed > 1:
			self.time_passed = 0
			truck = self.get_parent().get_node("follows").get_node("truck").duplicate()
			self.add_child(truck)
			truck.enabled = True

