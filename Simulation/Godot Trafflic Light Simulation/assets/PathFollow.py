from godot import exposed, export
from godot import *


@exposed
class PathFollow(PathFollow):

	# member variables here, example:
	enabled = export(bool, default=False)
	speed = export(int, default=10)
	path_0 = export(str)
	path_1 = export(str)

	def _ready(self):
		self.path_idx = 0;
		#self.paths =["cross", "out"]
		self.paths =[]
		self.visible = False
		
	def _process(self, delta):
		if self.enabled:

			self.visible = True
			progress = self.get_unit_offset()
			if progress >= 1:
					self.queue_free()
					self.enabled = False
			else:
				self.set_offset(self.get_offset() + self.speed * delta)
	
	def _on_Area_body_entered(self, body):
		self.speed = 0
		print('entered')
		
	def _on_Area_body_exited(self, body):
		self.speed = 10
		print('exited')


