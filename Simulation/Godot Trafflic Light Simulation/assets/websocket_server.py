import asyncio
import websockets
import json
import logging
import time
import threading




#asyncio.get_event_loop().run_forever()
from godot import exposed, export
from godot import *
@exposed
class websocket_server(Node):
	logging.basicConfig()

	STATE = {"value": 0}

	USERS = set()

	message_id = 0

	messages = []

	traffic_lights = []

	sensors = []

	oldsensors = []

	debug = False
	
	async def main_loop(self, websocket):
		global oldsensors
		while True:
			await asyncio.sleep(1)
			#await websocket.send("{\"msg_type\": \"test\", \"msg_id\": 5")
			#message = '{{"msg_type": "test", "msg_id": {0}}}'.format(new_messageid())
			#print(message)
			#await Send(websocket, message)
			for sensor in self.sensors:
				if (sensor.vehicles_coming or sensor.vehicles_waiting) and (traffic_light_by_id(sensor.id).state == "green"):
					sensor.vehicles_coming = False
					sensor.vehicles_waiting = False
			message = {
				"msg_id": self.new_messageid(),
				"msg_type": "notify_sensor_change",
				"data": [{"id": sensor.id, "vehicles_waiting": sensor.vehicles_waiting, "vehicles_coming": sensor.vehicles_coming, "vehicles_blocking": sensor.vehicles_blocking, "emergency_vehicle": sensor.emergency_vehicle, "public_transport": sensor.public_transport} for sensor in self.sensors]
			}
			await self.Send(websocket, json.dumps(message))

			if self.debug:
				print([(sensor.vehicles_coming or sensor.vehicles_waiting) for sensor in self.sensors])

	async def Receive(self, websocket):
		global message_id
		while True:
			try:
				async for jsonmessage in websocket:
					#print(jsonmessage)
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

	async def Send(self, websocket, message):
		jsonmessage = json.loads(message)
		print("<- | MSG #{0}, Type: {1}".format(jsonmessage["msg_id"], jsonmessage["msg_type"]))
		await websocket.send(message)

	def change_traffic_light_state(self, id, state):
		for i in range(0, len(self.traffic_lights)):
			if self.traffic_lights[i].id == id:
				self.traffic_lights[i].state = state
				self.change_state(id, state)

	def traffic_light_by_id(self, id):
		for tl in self.traffic_lights:
			if tl.id == id:
				return tl
		return self.TrafficLight(746, [], 746.0)

	def new_messageid(self):
		global message_id
		self.message_id = self.message_id + 1
		return self.message_id

	def initialization(self):
		self.traffic_lights.clear()
		crossingsstringlist = ["000000000000000000001111000100010000","000000000000000000000001000100010000","000000000000000000001110000000000000","000000000000000000001110000000000000","000000000000000000000001000100010000","000000000000000000000011101000100000","000000000000000000000010001000100000","000000000000000000000001100000000000","000000000000000000000001100000000000","000000000000000000000010001000100000","000000000000000000000100101111000000","000000000000000000000100100001000000","000000000000000000000000001110000000","000000000000000000000000001110000000","000000000000000000000100100001000000","000000000000000000001001000011110000","000000000000000000001001000010000000","000000000000000000000000000001110000","000000000000000000000000000001110000","000000000000000000001001000010000000","101100000000000110010001001111100000","101100000011001000000001101001100000","101101100100000000000000011000100000","110011011000000110011100011111110000","000001011011001000000100010001000000","000000000000000000000011101000100000","000001100110110000001111010001100000","110010000010110000001001000001110000","000000000010110110011001000000000000","000000000011001101101101101100000000","000001100100000101101111011100000000","110010000000000101100001000100000000","000000000000000000000000000000000110","000000000000000000000000000000001011","000000000000000000000000000000001101","000000000000000000000000000000000110"]
		for tlnr in range(0,36):
			crosses = []
			for x in range(0, len(crossingsstringlist)):
				if crossingsstringlist[tlnr][x] == '1':
					crosses.append(x + 1)
			self.traffic_lights.append(self.TrafficLight(tlnr + 1, crosses, 4.0))
		for i in [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25, 26, 27, 28, 31, 32, 33]:
			self.sensors.append(self.Sensor(i))
		if self.debug:
			for sensor in self.sensors:
				sensor.isOn = True
		message = {
			"msg_id": self.new_messageid(),
			"msg_type": "initialization",
			"data": [{"id": tl.id, "crosses": tl.crosses, "clearing_time": tl.clearing_time} for tl in self.traffic_lights]
		}
		return json.dumps(message)

	async def register(self, websocket):
		self.USERS.add(websocket)
		print("Client with ip: {0}:{1}".format(websocket.remote_address[0], websocket.remote_address[1]), "joined.")

	async def unregister(self, websocket):
		self.USERS.remove(websocket)

	async def counter(self, websocket, path):
		#starttime = time.time()
		await self.register(websocket)
		#while True:
		#    await asyncio.sleep(1)
		#    if not websocket.open:
		#        print(time.time() - starttime)
		await self.Send(websocket, self.initialization())
		#await Receive(websocket)

		try:
			await asyncio.gather(self.Receive(websocket), self.main_loop(websocket))
		except Exception as ex:
			print("Something went wrong while sending the initial message or in the main loop, someone likely disconnected.")
			print(type(ex).__name__, ex.args)
			await asyncio.sleep(1)
		finally:
			await self.unregister(websocket)

	class TrafficLight:
		def __init__(self, id, crosses, clearing_time):
			self.id = id
			self.crosses = crosses
			self.clearing_time = clearing_time
			self.state = "red"

	class Sensor:
		def __init__(self, id):
			self.id = id
			self.vehicles_waiting = False
			self.vehicles_coming = False
			self.vehicles_blocking = False
			self.emergency_vehicle = False
			self.public_transport = False
	
	def change_state(self, id, newstate):
		if len(self.actual_lights) >= id:
			for actual_light in self.actual_lights[id - 1]:
				if(newstate == "green"):
					actual_light.get_node("GreenLight").visible = True
					if actual_light.get_node("OrangeLight") != None:
						actual_light.get_node("OrangeLight").visible = False
					actual_light.get_node("RedLight").visible = False
				elif(newstate == "orange"):
					actual_light.get_node("GreenLight").visible = False
					if actual_light.get_node("OrangeLight") != None:
						actual_light.get_node("OrangeLight").visible = True
						actual_light.get_node("RedLight").visible = False
					else:
						actual_light.get_node("RedLight").visible = True
				elif(newstate == "red"):
					actual_light.get_node("GreenLight").visible = False
					if actual_light.get_node("OrangeLight") != None:
						actual_light.get_node("OrangeLight").visible = False
					actual_light.get_node("RedLight").visible = True
	
	def ready_actual_lights(self):
		self.actual_lights = []
		templist = []
		templist.append(self.find_parent("map").find_node("trafficlight1"))
		self.actual_lights.append(templist)
		templist = []
		templist.append(self.find_parent("map").find_node("trafficlight2"))
		self.actual_lights.append(templist)
		templist = []
		templist.append(self.find_parent("map").find_node("trafficlight3"))
		self.actual_lights.append(templist)
		templist = []
		templist.append(self.find_parent("map").find_node("trafficlight4"))
		self.actual_lights.append(templist)
		templist = []
		templist.append(self.find_parent("map").find_node("trafficlight5"))
		self.actual_lights.append(templist)
		templist = []
		templist.append(self.find_parent("map").find_node("trafficlight6"))
		self.actual_lights.append(templist)
		templist = []
		templist.append(self.find_parent("map").find_node("trafficlight7"))
		self.actual_lights.append(templist)
		templist = []
		templist.append(self.find_parent("map").find_node("trafficlight8"))
		self.actual_lights.append(templist)
		templist = []
		templist.append(self.find_parent("map").find_node("trafficlight9"))
		self.actual_lights.append(templist)
		templist = []
		templist.append(self.find_parent("map").find_node("trafficlight10"))
		self.actual_lights.append(templist)
		templist = []
		templist.append(self.find_parent("map").find_node("trafficlight11"))
		self.actual_lights.append(templist)
		templist = []
		templist.append(self.find_parent("map").find_node("trafficlight2"))
		self.actual_lights.append(templist)
		templist = []
		templist.append(self.find_parent("map").find_node("trafficlight13"))
		self.actual_lights.append(templist)
		templist = []
		templist.append(self.find_parent("map").find_node("trafficlight14"))
		self.actual_lights.append(templist)
		templist = []
		templist.append(self.find_parent("map").find_node("trafficlight15"))
		self.actual_lights.append(templist)
		templist = []
		templist.append(self.find_parent("map").find_node("trafficlight16"))
		self.actual_lights.append(templist)
		templist = []
		templist.append(self.find_parent("map").find_node("trafficlight17"))
		self.actual_lights.append(templist)
		templist = []
		templist.append(self.find_parent("map").find_node("trafficlight18"))
		self.actual_lights.append(templist)
		templist = []
		templist.append(self.find_parent("map").find_node("trafficlight19"))
		self.actual_lights.append(templist)
		templist = []
		templist.append(self.find_parent("map").find_node("trafficlight20"))
		self.actual_lights.append(templist)
		templist = []
		templist.append(self.find_parent("map").find_node("trafficlight21a"))
		templist.append(self.find_parent("map").find_node("trafficlight21b"))
		self.actual_lights.append(templist)
		templist = []
		templist.append(self.find_parent("map").find_node("trafficlight22a"))
		templist.append(self.find_parent("map").find_node("trafficlight22b"))
		self.actual_lights.append(templist)
		templist = []
		templist.append(self.find_parent("map").find_node("trafficlight23a"))
		templist.append(self.find_parent("map").find_node("trafficlight23b"))
		self.actual_lights.append(templist)
		templist = []
		templist.append(self.find_parent("map").find_node("trafficlight24a"))
		templist.append(self.find_parent("map").find_node("trafficlight24b"))
		self.actual_lights.append(templist)
		templist = []
		templist.append(self.find_parent("map").find_node("trafficlight25a"))
		templist.append(self.find_parent("map").find_node("trafficlight25b"))
		self.actual_lights.append(templist)
		templist = []
		templist.append(self.find_parent("map").find_node("trafficlight26a"))
		templist.append(self.find_parent("map").find_node("trafficlight26b"))
		self.actual_lights.append(templist)
		templist = []
		templist.append(self.find_parent("map").find_node("trafficlight27a"))
		templist.append(self.find_parent("map").find_node("trafficlight27b"))
		self.actual_lights.append(templist)
		templist = []
		templist.append(self.find_parent("map").find_node("trafficlight28a"))
		templist.append(self.find_parent("map").find_node("trafficlight28b"))
		self.actual_lights.append(templist)
		templist = []
		templist.append(self.find_parent("map").find_node("trafficlight29a"))
		templist.append(self.find_parent("map").find_node("trafficlight29b"))
		self.actual_lights.append(templist)
		templist = []
		templist.append(self.find_parent("map").find_node("trafficlight30"))
		self.actual_lights.append(templist)
		templist = []
		templist.append(self.find_parent("map").find_node("trafficlight31"))
		self.actual_lights.append(templist)
		templist = []
		templist.append(self.find_parent("map").find_node("trafficlight32"))
		self.actual_lights.append(templist)
		templist = []
		templist.append(self.find_parent("map").find_node("trafficlight33a"))
		templist.append(self.find_parent("map").find_node("trafficlight33b"))
		self.actual_lights.append(templist)
	
	def loopable(self):
		#wrapper around the even loop's create_server() method. It creates and starts a Server, then it wraps the server in a websocketserver and returns the websocketserver
		try:
			self.loop = asyncio.new_event_loop()
			asyncio.set_event_loop(self.loop)
			#start_server = websockets.serve(self.counter, port=6969, ping_interval=None, ping_timeout=None)
			#asyncio.get_event_loop().run_until_complete(start_server)
			asyncio.get_event_loop().run_until_complete(websockets.serve(self.counter, port=6969, ping_interval=None, ping_timeout=None))
			asyncio.get_event_loop().run_forever()
		#asyncio.get_event_loop().run_forever()
		except Exception as ex:
			print(ex)
		
	def _ready(self):
		self.ready_actual_lights()
		self.thread = threading.Thread(target=(self.loopable))
		self.thread.start()
	
	def _process(self, delta):
		pass
		#self.find_parent("map").get_node("tree_oak").visible = not self.find_parent("map").get_node("tree_oak").visible
