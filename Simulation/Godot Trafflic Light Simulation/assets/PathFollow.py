from godot import exposed, export
from godot import *
from math import cos

@exposed
class PathFollow(PathFollow):

	# member variables here, example:
	enabled = export(bool, default=False)
	speed = export(int, default=10)


	def _ready(self):
		self.path_idx = 0;
		#self.paths =["cross", "out"]
		self.paths =[]
		self.visible = False
		point = self.get_parent().get_curve().interpolate_baked(0)
		point2 = self.get_parent().get_curve().interpolate_baked(0.001)
		this_dir = (point2 - point).normalized()
		ref1 = Vector3(0.04706317558884621, -3.458734454397927e-06, -0.9988918900489807)
		ref2 = Vector3(-0.013520398177206516, -3.4035724638670217e-06, -0.9999085664749146)
		rad_to_deg = lambda r: (r / 3.1416) * 180
		
		ref_diff = rad_to_deg(ref1.angle_to(ref2))
		
		rad_ref1 = this_dir.angle_to(ref1)
		rad_ref2 = this_dir.angle_to(ref2)
		angle = rad_to_deg(rad_ref1)
		if rad_ref1 >= rad_ref2:
			self.set_rotation_degrees(Vector3(0,angle, 0))
		else:
			if ref_diff < angle < 180 - ref_diff :
				self.set_rotation_degrees(Vector3(0,angle+180, 0))
			else:
				self.set_rotation_degrees(Vector3(0,angle, 0))

		
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
		
		
	def _on_Area_body_exited(self, body):
		self.speed = 10


