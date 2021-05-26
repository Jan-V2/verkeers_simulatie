from godot import exposed, export
from godot import *
import websockets
import threading
import asyncio
import json
import time

@exposed
class websocket_server(Node):
	#Assigning some class variables
	STATE = {"value": 0}
	traffic_lights = []
	message_id = 0
	messages = []
	sensors = []
	
	#Main loop for sending sensors
	async def main_loop(self, websocket):
		while True:
			await asyncio.sleep(1)
			message = {
				"msg_id": self.new_messageid(),
				"msg_type": "notify_sensor_change",
				"data": [{"id": sensor.id, "vehicles_waiting": sensor.vehicles_waiting, "vehicles_coming": sensor.vehicles_coming, "vehicles_blocking": sensor.vehicles_blocking, "emergency_vehicle": sensor.emergency_vehicle, "public_vehicle": sensor.public_transport} for sensor in self.sensors]
			}
			await self.Send(websocket, json.dumps(message))

	#Receive loop
	async def Receive(self, websocket):
		global message_id
		while True:
			try:
				async for jsonmessage in websocket:
					#Parses incoming message and puts it through to the rest of the simulation
					message = json.loads(jsonmessage)
					self.messages.append(message)
					self.message_id = message["msg_id"]
					print("-> | MSG #{0}, Type: {1}".format(self.message_id, message["msg_type"]))
					if message["msg_type"] == "notify_traffic_light_change":
						for tl in message["data"]:
							self.change_traffic_light_state(tl["id"], tl["state"])
			except Exception as ex:
				print("Something went wrong in receiving and/or decoding a message.")
				print(type(ex).__name__, ex.args)
				await asyncio.sleep(1)

	#Sends a given message and prints some useful information
	async def Send(self, websocket, message):
		jsonmessage = json.loads(message)
		print("<- | MSG #{0}, Type: {1}".format(jsonmessage["msg_id"], jsonmessage["msg_type"]))
		await websocket.send(message)

	#Changes TrafficLight object and finally calls to change the actual traffic lights in the simulation
	def change_traffic_light_state(self, id, state):
		for i in range(0, len(self.traffic_lights)):
			if self.traffic_lights[i].id == id:
				self.traffic_lights[i].state = state
				self.change_state(id, state)

	#Returns the TrafficLight object for the given ID
	def traffic_light_by_id(self, id):
		for tl in self.traffic_lights:
			if tl.id == id:
				return tl
		return self.TrafficLight(746, [], 746.0)
	
	#Returns the Sensor object for the given ID
	def sensor_by_id(self, id):
		for sensor in self.sensors:
			if sensor.id == id:
				return sensor
		return self.Sensor(746)

	#Returns a fresh message ID
	def new_messageid(self):
		global message_id
		self.message_id = self.message_id + 1
		return self.message_id

	#Initializes lots of variables after connection happens and returns an "initialization" message
	def initialization(self):
		self.traffic_lights.clear()
		#This list contains every crossing of every traffic light and is converted to TrafficLight objects
		crossingsstringlist = ["000000000000000000001111000100010000","000000000000000000000001000100010000","000000000000000000001110000000000000","000000000000000000001110000000000000","000000000000000000000001000100010000","000000000000000000000011101000100000","000000000000000000000010001000100000","000000000000000000000001100000000000","000000000000000000000001100000000000","000000000000000000000010001000100000","000000000000000000000100101111000000","000000000000000000000100100001000000","000000000000000000000000001110000000","000000000000000000000000001110000000","000000000000000000000100100001000000","000000000000000000001001000011110000","000000000000000000001001000010000000","000000000000000000000000000001110000","000000000000000000000000000001110000","000000000000000000001001000010000000","101100000000000110010001001111100000","101100000011001000000001101001100000","101101100100000000000000011000100000","110011011000000110011100011111110000","000001011011001000000100010001000000","000000000000000000000011101000100000","000001100110110000001111010001100000","110010000010110000001001000001110000","000000000010110110011001000000000000","000000000011001101101101101100000000","000001100100000101101111011100000000","110010000000000101100001000100000000","000000000000000000000000000000000110","000000000000000000000000000000001011","000000000000000000000000000000001101","000000000000000000000000000000000110"]
		for tlnr in range(0,36):
			crosses = []
			for x in range(0, len(crossingsstringlist)):
				if crossingsstringlist[tlnr][x] == '1':
					crosses.append(x + 1)
			self.traffic_lights.append(self.TrafficLight(tlnr + 1, crosses, 4.0))
			self.traffic_light_by_id(34).clearing_time = 12
			self.traffic_light_by_id(35).clearing_time = 12
		#This initializes the sensors
		for i in [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25, 26, 28, 31, 32]:
			self.sensors.append(self.Sensor(i))
		#This creates the message and returns it
		message = {
			"msg_id": self.new_messageid(),
			"msg_type": "initialization",
			"data": [{"id": tl.id, "crosses": tl.crosses, "clearing_time": tl.clearing_time} for tl in self.traffic_lights]
		}
		return json.dumps(message)

	#Prints connection information to console
	async def register(self, websocket):
		print("Client with ip: {0}:{1}".format(websocket.remote_address[0], websocket.remote_address[1]), "joined.")

	#Handles the connection of a client and sets up the loops
	async def counter(self, websocket, path):
		await self.register(websocket)
		await self.Send(websocket, self.initialization())
		try:
			await asyncio.gather(self.Receive(websocket), self.main_loop(websocket))
		except Exception as ex:
			print("Something went wrong while sending the initial message or in the main loop, someone likely disconnected.")
			print(type(ex).__name__, ex.args)
			await asyncio.sleep(1)
	
	#Data class for keeping traffic light information
	class TrafficLight:
		def __init__(self, id, crosses, clearing_time):
			self.id = id
			self.crosses = crosses
			self.clearing_time = clearing_time
			self.state = "red"
			
	#Data class for keeping sensor information
	class Sensor:
		def __init__(self, id):
			self.id = id
			self.vehicles_waiting = False
			self.vehicles_coming = False
			self.vehicles_blocking = False
			self.emergency_vehicle = False
			self.public_transport = False
			
	# If you really want to know: If the boat traffic light goes to green, the
	# bridge will close. Since not everyone's controller has a long enough
	# green time for the boats to pass, the bridge needs to stay open for a bit
	# longer. Boats need about 5 seconds from start to finish to pass a bridge
	# so this starts a thread that will close the bridge 7 seconds after a light
	# switches from green.
	def bridge_close_thread_function_DONT_LOOK_AT_THIS(self):
		time.sleep(7)
		self.get_parent().find_node("bridge").going_up = False
	
	#This changes the state of a traffic light in the simulation by it's ID
	def change_state(self, id, newstate):
		if len(self.actual_lights) >= id:
			for actual_light in self.actual_lights[id - 1]:
				if(newstate == "green"):
					actual_light.get_node("GreenLight").visible = True
					if actual_light.get_node_or_null("OrangeLight") != None:
						actual_light.get_node("OrangeLight").visible = False
					actual_light.get_node("RedLight").visible = False
				elif(newstate == "orange"):
					actual_light.get_node("GreenLight").visible = False
					if actual_light.get_node_or_null("OrangeLight") != None:
						actual_light.get_node("OrangeLight").visible = True
						actual_light.get_node("RedLight").visible = False
					else:
						actual_light.get_node("RedLight").visible = True
				elif(newstate == "red"):
					actual_light.get_node("GreenLight").visible = False
					if actual_light.get_node_or_null("OrangeLight") != None:
						actual_light.get_node("OrangeLight").visible = False
					actual_light.get_node("RedLight").visible = True
		#This makes sure that the bridge moves along
		if id == 34 or id == 35:
			if newstate == "green":
				self.get_parent().find_node("bridge").going_up = True
			elif newstate == "orange":
				self.thread = threading.Thread(target=(self.bridge_close_thread_function_DONT_LOOK_AT_THIS))
				self.thread.start()
	
	#This keeps track of the traffic lights inside the simulation and makes it easy to cycle through them
	def ready_actual_lights(self):
		self.actual_lights = []
		templist = []
		templist.append(self.get_parent().find_node("trafficlight1"))
		self.actual_lights.append(templist)
		templist = []
		templist.append(self.get_parent().find_node("trafficlight2"))
		self.actual_lights.append(templist)
		templist = []
		templist.append(self.get_parent().find_node("trafficlight3"))
		self.actual_lights.append(templist)
		templist = []
		templist.append(self.get_parent().find_node("trafficlight4"))
		self.actual_lights.append(templist)
		templist = []
		templist.append(self.get_parent().find_node("trafficlight5"))
		self.actual_lights.append(templist)
		templist = []
		templist.append(self.get_parent().find_node("trafficlight6"))
		self.actual_lights.append(templist)
		templist = []
		templist.append(self.get_parent().find_node("trafficlight7"))
		self.actual_lights.append(templist)
		templist = []
		templist.append(self.get_parent().find_node("trafficlight8"))
		self.actual_lights.append(templist)
		templist = []
		templist.append(self.get_parent().find_node("trafficlight9"))
		self.actual_lights.append(templist)
		templist = []
		templist.append(self.get_parent().find_node("trafficlight10"))
		self.actual_lights.append(templist)
		templist = []
		templist.append(self.get_parent().find_node("trafficlight11"))
		self.actual_lights.append(templist)
		templist = []
		templist.append(self.get_parent().find_node("trafficlight12"))
		self.actual_lights.append(templist)
		templist = []
		templist.append(self.get_parent().find_node("trafficlight13"))
		self.actual_lights.append(templist)
		templist = []
		templist.append(self.get_parent().find_node("trafficlight14"))
		self.actual_lights.append(templist)
		templist = []
		templist.append(self.get_parent().find_node("trafficlight15"))
		self.actual_lights.append(templist)
		templist = []
		templist.append(self.get_parent().find_node("trafficlight16"))
		self.actual_lights.append(templist)
		templist = []
		templist.append(self.get_parent().find_node("trafficlight17"))
		self.actual_lights.append(templist)
		templist = []
		templist.append(self.get_parent().find_node("trafficlight18"))
		self.actual_lights.append(templist)
		templist = []
		templist.append(self.get_parent().find_node("trafficlight19"))
		self.actual_lights.append(templist)
		templist = []
		templist.append(self.get_parent().find_node("trafficlight20"))
		self.actual_lights.append(templist)
		templist = []
		templist.append(self.get_parent().find_node("trafficlight21a"))
		templist.append(self.get_parent().find_node("trafficlight21b"))
		self.actual_lights.append(templist)
		templist = []
		templist.append(self.get_parent().find_node("trafficlight22a"))
		templist.append(self.get_parent().find_node("trafficlight22b"))
		self.actual_lights.append(templist)
		templist = []
		templist.append(self.get_parent().find_node("trafficlight23a"))
		templist.append(self.get_parent().find_node("trafficlight23b"))
		self.actual_lights.append(templist)
		templist = []
		templist.append(self.get_parent().find_node("trafficlight24a"))
		templist.append(self.get_parent().find_node("trafficlight24b"))
		self.actual_lights.append(templist)
		templist = []
		templist.append(self.get_parent().find_node("trafficlight25a"))
		templist.append(self.get_parent().find_node("trafficlight25b"))
		self.actual_lights.append(templist)
		templist = []
		templist.append(self.get_parent().find_node("trafficlight26a"))
		templist.append(self.get_parent().find_node("trafficlight26b"))
		self.actual_lights.append(templist)
		templist = []
		templist.append(self.get_parent().find_node("trafficlight27a"))
		templist.append(self.get_parent().find_node("trafficlight27b"))
		self.actual_lights.append(templist)
		templist = []
		templist.append(self.get_parent().find_node("trafficlight28a"))
		templist.append(self.get_parent().find_node("trafficlight28b"))
		self.actual_lights.append(templist)
		templist = []
		templist.append(self.get_parent().find_node("trafficlight29a"))
		templist.append(self.get_parent().find_node("trafficlight29b"))
		self.actual_lights.append(templist)
		templist = []
		templist.append(self.get_parent().find_node("trafficlight30"))
		self.actual_lights.append(templist)
		templist = []
		templist.append(self.get_parent().find_node("trafficlight31"))
		self.actual_lights.append(templist)
		templist = []
		templist.append(self.get_parent().find_node("trafficlight32"))
		self.actual_lights.append(templist)
		templist = []
		templist.append(self.get_parent().find_node("trafficlight33a"))
		templist.append(self.get_parent().find_node("trafficlight33b"))
		self.actual_lights.append(templist)
		templist = []
		templist.append(self.get_parent().find_node("trafficlight34a"))
		templist.append(self.get_parent().find_node("trafficlight34b"))
		self.actual_lights.append(templist)
		templist = []
		templist.append(self.get_parent().find_node("trafficlight35a"))
		templist.append(self.get_parent().find_node("trafficlight35b"))
		self.actual_lights.append(templist)
	
	#We don't like this part. These connect the sensor signals to the Sensor objects in this script. This will not work from within the sensors itself, which would be cleaner, because you can only reach "simple" variables from outside classes in Godot.
	def _on_target819_body_shape_entered(self, arg1, arg2, arg3, arg4):
		#sensor 1
		self.sensor_by_id(1).vehicles_waiting = True
		
	def _on_target819_body_shape_exited(self, arg1, arg2, arg3, arg4):
		#sensor 1
		self.sensor_by_id(1).vehicles_waiting = False
		
	def _on_target919_body_shape_entered(self, arg1, arg2, arg3, arg4):
		#sensor 2
		self.sensor_by_id(2).vehicles_waiting = True
		
	def _on_target919_body_shape_exited(self, arg1, arg2, arg3, arg4):
		#sensor 2
		self.sensor_by_id(2).vehicles_waiting = False
		
	def _on_target1019_body_shape_entered(self, arg1, arg2, arg3, arg4):
		#sensor 3
		self.sensor_by_id(3).vehicles_waiting = True
		
	def _on_target1019_body_shape_exited(self, arg1, arg2, arg3, arg4):
		#sensor 3
		self.sensor_by_id(3).vehicles_waiting = False
		
	def _on_target1119_body_shape_entered(self, arg1, arg2, arg3, arg4):
		#sensor 4
		self.sensor_by_id(4).vehicles_waiting = True
		
	def _on_target1119_body_shape_exited(self, arg1, arg2, arg3, arg4):
		#sensor 4
		self.sensor_by_id(4).vehicles_waiting = False
		
	def _on_target1520_body_shape_entered(self, arg1, arg2, arg3, arg4):
		#sensor 5
		self.sensor_by_id(5).vehicles_waiting = True
		
	def _on_target1520_body_shape_exited(self, arg1, arg2, arg3, arg4):
		#sensor 5
		self.sensor_by_id(5).vehicles_waiting = False
		
	def _on_target1521_body_shape_entered(self, arg1, arg2, arg3, arg4):
		#sensor 6
		self.sensor_by_id(6).vehicles_waiting = True
		
	def _on_target1521_body_shape_exited(self, arg1, arg2, arg3, arg4):
		#sensor 6
		self.sensor_by_id(6).vehicles_waiting = False
		
	def _on_target1522_body_shape_entered(self, arg1, arg2, arg3, arg4):
		#sensor 7
		self.sensor_by_id(7).vehicles_waiting = True
		
	def _on_target1522_body_shape_exited(self, arg1, arg2, arg3, arg4):
		#sensor 7
		self.sensor_by_id(7).vehicles_waiting = False
		
	def _on_target723_body_shape_entered(self, arg1, arg2, arg3, arg4):
		#sensor 8
		self.sensor_by_id(8).vehicles_waiting = True
		
	def _on_target723_body_shape_exited(self, arg1, arg2, arg3, arg4):
		#sensor 8
		self.sensor_by_id(8).vehicles_waiting = False
		
	def _on_target724_body_shape_entered(self, arg1, arg2, arg3, arg4):
		#sensor 9
		self.sensor_by_id(9).vehicles_waiting = True
		
	def _on_target724_body_shape_exited(self, arg1, arg2, arg3, arg4):
		#sensor 9
		self.sensor_by_id(9).vehicles_waiting = False
		
	def _on_target725_body_shape_entered(self, arg1, arg2, arg3, arg4):
		#sensor 10
		self.sensor_by_id(10).vehicles_waiting = True
		
	def _on_target725_body_shape_exited(self, arg1, arg2, arg3, arg4):
		#sensor 10
		self.sensor_by_id(10).vehicles_waiting = False
		
	def _on_target1126_body_shape_entered(self, arg1, arg2, arg3, arg4):
		#sensor 11
		self.sensor_by_id(11).vehicles_waiting = True
		
	def _on_target1126_body_shape_exited(self, arg1, arg2, arg3, arg4):
		#sensor 11
		self.sensor_by_id(11).vehicles_waiting = False
		
	def _on_target1226_body_shape_entered(self, arg1, arg2, arg3, arg4):
		#sensor 12
		self.sensor_by_id(12).vehicles_waiting = True
		
	def _on_target1226_body_shape_exited(self, arg1, arg2, arg3, arg4):
		#sensor 12
		self.sensor_by_id(12).vehicles_waiting = False
		
	def _on_target1326_body_shape_entered(self, arg1, arg2, arg3, arg4):
		#sensor 13
		self.sensor_by_id(13).vehicles_waiting = True
		
	def _on_target1326_body_shape_exited(self, arg1, arg2, arg3, arg4):
		#sensor 13
		self.sensor_by_id(13).vehicles_waiting = False
		
	def _on_target1426_body_shape_entered(self, arg1, arg2, arg3, arg4):
		#sensor 14
		self.sensor_by_id(14).vehicles_waiting = True
		
	def _on_target1426_body_shape_exited(self, arg1, arg2, arg3, arg4):
		#sensor 14
		self.sensor_by_id(14).vehicles_waiting = False
		
	def _on_s15_body_shape_entered(self, arg1, arg2, arg3, arg4):
		#sensor 15
		self.sensor_by_id(15).vehicles_waiting = True
		
	def _on_s15_body_shape_exited(self, arg1, arg2, arg3, arg4):
		#sensor 15
		self.sensor_by_id(15).vehicles_waiting = False
		
	def _on_s16_body_shape_entered(self, arg1, arg2, arg3, arg4):
		#sensor 16
		self.sensor_by_id(16).vehicles_waiting = True
		
	def _on_s16_body_shape_exited(self, arg1, arg2, arg3, arg4):
		#sensor 16
		self.sensor_by_id(16).vehicles_waiting = False
		
	def _on_s17_body_shape_entered(self, arg1, arg2, arg3, arg4):
		#sensor 17
		self.sensor_by_id(17).vehicles_waiting = True
		
	def _on_s17_body_shape_exited(self, arg1, arg2, arg3, arg4):
		#sensor 17
		self.sensor_by_id(17).vehicles_waiting = False
		
	def _on_s18_body_shape_entered(self, arg1, arg2, arg3, arg4):
		#sensor 18
		self.sensor_by_id(18).vehicles_waiting = True
		
	def _on_s18_body_shape_exited(self, arg1, arg2, arg3, arg4):
		#sensor 18
		self.sensor_by_id(18).vehicles_waiting = False
		
	def _on_s19_body_shape_entered(self, arg1, arg2, arg3, arg4):
		#sensor 19
		self.sensor_by_id(19).vehicles_waiting = True
		
	def _on_s19_body_shape_exited(self, arg1, arg2, arg3, arg4):
		#sensor 19
		self.sensor_by_id(19).vehicles_waiting = False
		
	def _on_s20_body_shape_entered(self, arg1, arg2, arg3, arg4):
		#sensor 20
		self.sensor_by_id(20).vehicles_waiting = True
		
	def _on_s20_body_shape_exited(self, arg1, arg2, arg3, arg4):
		#sensor 20
		self.sensor_by_id(20).vehicles_waiting = False
		
	def _on_s21_body_shape_entered(self, arg1, arg2, arg3, arg4):
		#sensor 21
		self.sensor_by_id(21).vehicles_waiting = True
		
	def _on_s21_body_shape_exited(self, arg1, arg2, arg3, arg4):
		#sensor 21
		self.sensor_by_id(21).vehicles_waiting = False
		
	def _on_s21c_body_shape_entered(self, arg1, arg2, arg3, arg4):
		#sensor 21
		self.sensor_by_id(21).vehicles_coming = True
		
	def _on_s21c_body_shape_exited(self, arg1, arg2, arg3, arg4):
		#sensor 21
		self.sensor_by_id(21).vehicles_coming = False
		
	def _on_s22_body_shape_entered(self, arg1, arg2, arg3, arg4):
		#sensor 22
		self.sensor_by_id(22).vehicles_waiting = True
		
	def _on_s22_body_shape_exited(self, arg1, arg2, arg3, arg4):
		#sensor 22
		self.sensor_by_id(22).vehicles_waiting = False
		
	def _on_s22c_body_shape_entered(self, arg1, arg2, arg3, arg4):
		#sensor 22
		self.sensor_by_id(22).vehicles_coming = True
		
	def _on_s22c_body_shape_exited(self, arg1, arg2, arg3, arg4):
		#sensor 22
		self.sensor_by_id(22).vehicles_coming = False
		
	def _on_s23_body_shape_entered(self, arg1, arg2, arg3, arg4):
		#sensor 23
		self.sensor_by_id(23).vehicles_waiting = True
		
	def _on_s23_body_shape_exited(self, arg1, arg2, arg3, arg4):
		#sensor 23
		self.sensor_by_id(23).vehicles_waiting = False
		
	def _on_s23c_body_shape_entered(self, arg1, arg2, arg3, arg4):
		#sensor 23
		self.sensor_by_id(23).vehicles_coming = True
		
	def _on_s23c_body_shape_exited(self, arg1, arg2, arg3, arg4):
		#sensor 23
		self.sensor_by_id(23).vehicles_coming = False
		
	def _on_s24_body_shape_entered(self, arg1, arg2, arg3, arg4):
		#sensor 24
		self.sensor_by_id(24).vehicles_waiting = True
		
	def _on_s24_body_shape_exited(self, arg1, arg2, arg3, arg4):
		#sensor 24
		self.sensor_by_id(24).vehicles_waiting = False
		
	def _on_s24c_body_shape_entered(self, arg1, arg2, arg3, arg4):
		#sensor 24
		self.sensor_by_id(24).vehicles_coming = True
		
	def _on_s24c_body_shape_exited(self, arg1, arg2, arg3, arg4):
		#sensor 24
		self.sensor_by_id(24).vehicles_coming = False
		
	def _on_s25_body_shape_entered(self, arg1, arg2, arg3, arg4):
		#sensor 25
		self.sensor_by_id(25).vehicles_waiting = True
		
	def _on_s25_body_shape_exited(self, arg1, arg2, arg3, arg4):
		#sensor 25
		self.sensor_by_id(25).vehicles_waiting = False
		
	def _on_s25c_body_shape_entered(self, arg1, arg2, arg3, arg4):
		#sensor 25
		self.sensor_by_id(25).vehicles_coming = True
		
	def _on_s25c_body_shape_exited(self, arg1, arg2, arg3, arg4):
		#sensor 25
		self.sensor_by_id(25).vehicles_coming = False
		
	def _on_s26_body_shape_entered(self, arg1, arg2, arg3, arg4):
		#sensor 26
		self.sensor_by_id(26).vehicles_waiting = True
		self.sensor_by_id(26).public_transport = True
		
	def _on_s26_body_shape_exited(self, arg1, arg2, arg3, arg4):
		#sensor 26
		self.sensor_by_id(26).vehicles_waiting = False
		self.sensor_by_id(26).public_transport = False
		
	def _on_s28_body_shape_entered(self, arg1, arg2, arg3, arg4):
		#sensor 28
		self.sensor_by_id(28).vehicles_waiting = True
		
	def _on_s28_body_shape_exited(self, arg1, arg2, arg3, arg4):
		#sensor 28
		self.sensor_by_id(28).vehicles_waiting = False
		
	def _on_s31_body_shape_entered(self, arg1, arg2, arg3, arg4):
		#sensor 31
		self.sensor_by_id(31).vehicles_waiting = True
		
	def _on_s31_body_shape_exited(self, arg1, arg2, arg3, arg4):
		#sensor 31
		self.sensor_by_id(31).vehicles_waiting = False
		
	def _on_s31c_body_shape_entered(self, arg1, arg2, arg3, arg4):
		#sensor 31
		self.sensor_by_id(31).vehicles_coming = True
		
	def _on_s31c_body_shape_exited(self, arg1, arg2, arg3, arg4):
		#sensor 31
		self.sensor_by_id(31).vehicles_coming = False
		
	def _on_s32_body_shape_entered(self, arg1, arg2, arg3, arg4):
		#sensor 32
		self.sensor_by_id(32).vehicles_waiting = True
		
	def _on_s32_body_shape_exited(self, arg1, arg2, arg3, arg4):
		#sensor 32
		self.sensor_by_id(32).vehicles_waiting = False
		
	def _on_s32c_body_shape_entered(self, arg1, arg2, arg3, arg4):
		#sensor 32
		self.sensor_by_id(32).vehicles_coming = True
		
	def _on_s32c_body_shape_exited(self, arg1, arg2, arg3, arg4):
		#sensor 32
		self.sensor_by_id(32).vehicles_coming = False
		
	def _on_s33_body_shape_entered(self, arg1, arg2, arg3, arg4):
		#sensor 33
		self.sensor_by_id(22).vehicles_blocking = True
		self.sensor_by_id(25).vehicles_blocking = True
		self.sensor_by_id(30).vehicles_blocking = True
		
	def _on_s33_body_shape_exited(self, arg1, arg2, arg3, arg4):
		#sensor 33
		self.sensor_by_id(22).vehicles_blocking = False
		self.sensor_by_id(25).vehicles_blocking = False
		self.sensor_by_id(30).vehicles_blocking = False
	
	#This makes sure that the websocket side of the simulation will keep running continuously and asynchronously
	def loopable(self):
		try:
			self.loop = asyncio.new_event_loop()
			asyncio.set_event_loop(self.loop)
			asyncio.get_event_loop().run_until_complete(websockets.serve(self.counter, port=6969, ping_interval=None, ping_timeout=None))
			asyncio.get_event_loop().run_forever()
		except Exception as ex:
			print(ex)
		
	#This readies all the traffic lights in the simulation, turns them red (because not everyone's controller will do this themselves) and starts the websocket thread
	def _ready(self):
		self.ready_actual_lights()
		for i in range(1,36):
			self.change_state(i, "red")
		self.thread = threading.Thread(target=(self.loopable))
		self.thread.start()
