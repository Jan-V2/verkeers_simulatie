from godot import exposed, export, ResourceLoader
from godot import *
from random import choice

@exposed
class path(Path):
	def _ready(self):
		self.testing_lights = True
		
		self.time_passed_car = 0
		self.time_passed_boat = 0
		self.new_bus = ResourceLoader.load("res://assets/path_schoolbus.tscn")
		self.test_car = ResourceLoader.load("res://assets/path_firetruck.tscn")
		self.new_cars = [ResourceLoader.load("res://assets/path_delivery.tscn"),
			ResourceLoader.load("res://assets/path_deliveryFlat.tscn"),
			ResourceLoader.load("res://assets/path_garbageTruck.tscn"),
			ResourceLoader.load("res://assets/path_sedan.tscn"),
			ResourceLoader.load("res://assets/path_SUV.tscn"),
			ResourceLoader.load("res://assets/path_taxi.tscn"),
			ResourceLoader.load("res://assets/path_tractor.tscn"),
			ResourceLoader.load("res://assets/path_van.tscn"),
			]
		self.paths =['N->W','N->E','N->S1','N->S2','N->E','E->N1','E->N2','E->W','E->S', "E->E",'W->N','W->E','W->S','S->W','S->N1','S->N2','S->E',]
		self.path_idx = 0
		
		self.time_passed_fiets = 0
		self.fiets_max = 6
		self.fiets_idx = 0
		self.fiets_speed = 3
		self.fietsers = [ResourceLoader.load("res://assets/path_bikervampire.tscn"),
							ResourceLoader.load("res://assets/path_bikerzombie.tscn"),
							ResourceLoader.load("res://assets/path_bikerskeleton.tscn")]
		
		self.time_passed_voet = 0
		self.voet_max = 6
		self.voet_idx = 0
		self.voet_speed = 3
		self.voeters = [ResourceLoader.load("res://assets/path_vampire.tscn"),
							ResourceLoader.load("res://assets/path_zombie.tscn"),
							ResourceLoader.load("res://assets/path_skeleton.tscn")]
		
		self.boat_spawn_dir = False
		self.boat_idx = 0
		self.boats_max = 10
		self.boat_speed = 3
		self.boat_models = []
		for i in range(self.boats_max):
			self.boat_models.append(ResourceLoader.load("res://assets/boats/boat{}.tscn".format(i)))
		
	def _process(self, delta):
		self.time_passed_car += delta
		if self.time_passed_car > 3:
			self.time_passed_car = 0
			path = self.paths[self.path_idx]
			if path == 'E->E':
				car = self.new_bus.instance()
				self.get_parent().get_node(path).add_child(car)
				car.enabled = True
			else:
				truck = choice(self.new_cars).instance()
				self.get_parent().get_node(self.paths[self.path_idx]).add_child(truck)
				#self.get_parent().get_node("N->S1").add_child(truck)
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
			boat.speed = self.boat_speed
			boat.enabled = True
			#self.boat_spawn_dir = not self.boat_spwan_dir
			self.boat_idx += 1
			if not self.boat_idx < self.boats_max:
				self.boat_idx = 0;
		
		self.time_passed_fiets += delta
		if self.time_passed_fiets > 10:
			self.time_passed_fiets = 0
			fiets = choice(self.fietsers).instance()
			self.get_parent().get_node("fiets{}".format(self.fiets_idx)).add_child(fiets)
			fiets.speed = 3
			fiets.normal_speed = 3
			fiets.enabled = True
			self.fiets_idx += 1
			if not self.fiets_idx < self.fiets_max:
				self.fiets_idx = 0;
				
		self.time_passed_voet += delta
		if self.time_passed_voet > 10:
			self.time_passed_voet = 0
			voet = choice(self.voeters).instance()
			self.get_parent().get_node("voet{}".format(self.voet_idx)).add_child(voet)
			if self.voet_idx == 5:
				rotation = voet.get_rotation()
				rotation.y += (180 * 0.0174533)
				voet.set_rotation(rotation)
			voet.speed = voet.speed = 3
			voet.normal_speed = 3
			voet.enabled = True
			self.voet_idx += 1
			if not self.voet_idx < self.voet_max:
				self.voet_idx = 0;
				

	def _on_Area_body_entered(one, two):
		print("entered area")
