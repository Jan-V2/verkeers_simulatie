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
		self.paths =[['8,15|8,19', ['N->E', '22,25|15,25']],['9,15|9,19', ['N->S1', '8,31|8,26']],['10,15|10,19', ['N->S2', '9,31|9,26']],['11,15|11,19', ['N->E', '22,25|15,25']],['22,20|15,20', ['E->N1', '14,15|14,19']],['22,21|15,21', ['E->N2', '13,15|13,19']],['0,23|7,23', ['W->N', '13,15|13,19']],['0,24|7,24', ['W->E', '22,25|15,25']],['0,25|7,25', ['W->S', '8,31|8,26']],['11,31|11,26', ['S->W',  '0,21|7,21']],['12,31|12,26', ['S->N1', '13,15|13,19']],['13,31|13,26', ['S->N2', '14,15|14,19']],['14,31|14,26', ['S->E', '22,25|15,25']],]
		self.paths2 =['N->E','N->S1','N->S2','N->E','E->N1','E->N2','E->W','E->S','W->N','W->E','W->S','S->W','S->N1','S->N2','S->E',]
		
	
		
	def _process(self, delta):
		self.time_passed += delta
		if self.time_passed > 2:
			self.time_passed = 0
			truck = self.new_truck.instance()
			path = choice(self.paths2)
			self.get_parent().get_node(path).add_child(truck)
			#truck.path_0 = path[1][0]
			#truck.path_1 = path[1][1]

			truck.enabled = True
	
	def _on_Area_body_entered(one, two):
		print("entered area")
