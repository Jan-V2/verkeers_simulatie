from godot import exposed, export, ResourceLoader
from godot import *
from random import choice

@exposed
class path(Path):
	def _ready(self):
		self.time_passed_car = 0
		self.time_passed_boat = 0
		self.new_bus = ResourceLoader.load("res://assets/path_van.tscn")
		self.new_truck = ResourceLoader.load("res://assets/path_truck.tscn")
		self.paths =['N->W','N->E','N->S1','N->S2','N->E','E->N1','E->N2','E->W','E->S', "E->E",'W->N','W->E','W->S','S->W','S->N1','S->N2','S->E',]
		self.path_idx = 0
		
		self.boat_spawn_dir = False
		self.boat_idx = 0
		self.boats_max = 10
		self.boat_models = []
		for i in range(self.boats_max):
			self.boat_models.append(ResourceLoader.load("res://assets/boats/boat{}.tscn".format(i)))
		
	def _process(self, delta):
		self.time_passed_car += delta
		if self.time_passed_car > 2:
			self.time_passed_car = 0
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
		
		self.time_passed_boat += delta
		if self.time_passed_boat > 30:
			self.time_passed_boat = 0
			boat = self.boat_models[self.boat_idx].instance()
			if self.boat_spawn_dir:
				self.get_parent().get_node("boot_heen").add_child(boat)
				self.boat_spawn_dir = False
			else:
				self.get_parent().get_node("boot_weer").add_child(boat)
				self.boat_spawn_dir =  True
			boat.enabled = True
			#self.boat_spawn_dir = not self.boat_spwan_dir
			self.boat_idx += 1
			if not self.boat_idx < self.boats_max:
				self.boat_idx = 0;

	def _on_Area_body_entered(one, two):
		print("entered area")
