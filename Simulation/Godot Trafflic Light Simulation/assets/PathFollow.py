from godot import exposed, export
from godot import *


@exposed
class PathFollow(PathFollow):

	# member variables here, example:
	a = export(int, default=10)


	def _ready(self):
		pass
		
	def _process(self, delta):
		self.set_offset(self.get_offset() + self.a * delta)
