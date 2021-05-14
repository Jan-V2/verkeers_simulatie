from godot import exposed, export
from godot import *


@exposed
class PathFollow(PathFollow):

	# member variables here, example:
	enabled = export(bool, default=False)

	def _ready(self):
		self.path_idx = 0;
		self.paths =["cross", "out"]
		self.speed = 10
		self.visible = False
		
	def _process(self, delta):
		if self.enabled:
			self.visible = True
			progress = self.get_unit_offset()
			if progress >= 1:
				if self.path_idx >= len(self.paths):
					self.queue_free()
				else:
					self.set_unit_offset(0)
					new_parent = self.get_parent().get_parent().get_node(self.paths[self.path_idx])
					self.get_parent().remove_child(self)
					new_parent.add_child(self)
					self.path_idx += 1
			else:
				self.set_offset(self.get_offset() + self.speed * delta)
