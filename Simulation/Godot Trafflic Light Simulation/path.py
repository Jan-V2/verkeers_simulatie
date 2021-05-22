from godot import exposed, export, ResourceLoader
from godot import *
from random import choice

@exposed
class path(Path):
	def _ready(self):
		self.time_passed = 0
		self.new_bus = ResourceLoader.load("res://assets/path_van.tscn")
		self.new_truck = ResourceLoader.load("res://assets/path_truck.tscn")
		self.paths =['N->W','N->E','N->S1','N->S2','N->E','E->N1','E->N2','E->W','E->S', "E->E",'W->N','W->E','W->S','S->W','S->N1','S->N2','S->E',]
		self.path_idx = 0


	def _process(self, delta):
		self.time_passed += delta
		if self.time_passed > 2:
			self.time_passed = 0
			path = self.paths[self.path_idx]
			if path == 'E->E':
				car = self.new_bus.instance()
				self.get_parent().get_node(path).add_child(car)
				car.enabled = True
			else:
				truck = self.new_truck.instance()
				self.get_parent().get_node(self.paths[self.path_idx]).add_child(truck)
				truck.enabled = True
		self.path_idx += 1
		if not self.path_idx < len(self.paths):
			self.path_idx = 0

	def _on_Area_body_entered(one, two):
		print("entered area")
