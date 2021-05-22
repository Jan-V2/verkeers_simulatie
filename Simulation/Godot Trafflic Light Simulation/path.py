from godot import exposed, export, ResourceLoader
from godot import *
from random import choice

@exposed
class path(Path):

	# member variables here, example:
	a = export(int)
	b = export(str, default='foo')

	def _ready(self):
		self.time_passed = 0
		self.new_truck = ResourceLoader.load("res://assets/path_truck.tscn")
		self.paths =['N->W','N->E','N->S1','N->S2','N->E','E->N1','E->N2','E->W','E->S','W->N','W->E','W->S','S->W','S->N1','S->N2','S->E',]
		self.path_idx = 0
	
		
	def _process(self, delta):
		self.time_passed += delta
		if self.time_passed > 1:
			self.time_passed = 0
			truck = self.new_truck.instance()
			#path = choice(self.paths2)
			print(self.paths[self.path_idx])
			self.get_parent().get_node(self.paths[self.path_idx]).add_child(truck)
			
			self.path_idx += 1
			if not self.path_idx < len(self.paths):
				self.path_idx = 0
			
			#truck.path_0 = path[1][0]
			#truck.path_1 = path[1][1]

			truck.enabled = True
	
	def _on_Area_body_entered(one, two):
		print("entered area")
