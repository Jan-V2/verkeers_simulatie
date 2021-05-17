from godot import exposed, export, ResourceLoader
from godot import *


@exposed
class path(Path):

	# member variables here, example:
	a = export(int)
	b = export(str, default='foo')

	def _ready(self):
		self.time_passed = 0
		self.new_truck = ResourceLoader.load("res://assets/path_truck.tscn")
		pass
		
	def _process(self, delta):
		self.time_passed += delta
		if self.time_passed > 1:
			self.time_passed = 0
			truck = self.new_truck.instance()
			self.add_child(truck)
			truck.enabled = True
	
	def _on_Area_body_entered(one, two):
		print("entered area")
