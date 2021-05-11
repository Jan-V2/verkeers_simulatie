from godot import exposed, export, ResourceLoader
from godot import *

dinges = ResourceLoader.load("res://assets/sedan.tscn")


@exposed
class Carspawner(Node):

	# member variables here, example:
	a = export(int)
	b = export(str, default='foo')
	c = []

	def _ready(self):
		newcar = dinges.instance()
		newcar.name = "test"
		self.add_child(newcar)
	
	def _process(self, delta):
		self.get_node("test").move_and_slide(Vector3(0,1,0))
		pass
		
