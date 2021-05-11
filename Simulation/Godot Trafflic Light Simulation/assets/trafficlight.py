from godot import exposed, export
from godot import *
import time


@exposed
class trafficlight(Spatial):

	# member variables here, example:
	a = export(int)
	b = export(str, default='foo')
	state = "Green"
	lastchanged = round(time.time())

	def _ready(self):
		"""
		Called every time the node is added to the scene.
		Initialization here.
		"""
		pass
		
	def change_state(self, newstate):
			if(newstate == "Green"):
				self.state = "Green"
				self.get_node("GreenLight").visible = True
				self.get_node("OrangeLight").visible = False
				self.get_node("RedLight").visible = False
			elif(newstate == "Orange"):
				self.state = "Orange"
				self.get_node("GreenLight").visible = False
				self.get_node("OrangeLight").visible = True
				self.get_node("RedLight").visible = False
			elif(newstate == "Red"):
				self.state = "Red"
				self.get_node("GreenLight").visible = False
				self.get_node("OrangeLight").visible = False
				self.get_node("RedLight").visible = True
		
	def _process(self, delta):
		if (round(time.time()) != self.lastchanged):
			if(self.state == "Green"):
				self.change_state("Orange")
			elif(self.state == "Orange"):
				self.change_state("Red")
			elif(self.state == "Red"):
				self.change_state("Green")
			self.lastchanged = round(time.time())

