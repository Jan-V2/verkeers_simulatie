from godot import exposed, export
from godot import *
import time


@exposed
class trafficlight(Spatial):

	# member variables here, example:
	a = export(int)
	b = export(str, default='foo')
	state = "red"
	lastchanged = round(time.time())

	def _ready(self):
		"""
		Called every time the node is added to the scene.
		Initialization here.
		"""
		self.change_state("red")
		
	def change_state(self, newstate):
		if(newstate == "green"):
			self.state = "green"
			self.get_node("GreenLight").visible = True
			self.get_node("OrangeLight").visible = False
			self.get_node("RedLight").visible = False
		elif(newstate == "orange"):
			self.state = "orange"
			self.get_node("GreenLight").visible = False
			self.get_node("OrangeLight").visible = True
			self.get_node("RedLight").visible = False
		elif(newstate == "red"):
			self.state = "red"
			self.get_node("GreenLight").visible = False
			self.get_node("OrangeLight").visible = False
			self.get_node("RedLight").visible = True
		
	def _process(self, delta):
		pass

