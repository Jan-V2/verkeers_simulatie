import asyncio
import websockets
import json
import logging
import time

logging.basicConfig()

STATE = {"value": 0}

USERS = set()

message_id = 0

messages = []

traffic_lights = []

sensors = []

oldsensors = []

debug = False

async def main_loop(websocket):
    global oldsensors
    while True:
        await asyncio.sleep(1)
        #await websocket.send("{\"msg_type\": \"test\", \"msg_id\": 5")
        #message = '{{"msg_type": "test", "msg_id": {0}}}'.format(new_messageid())
        #print(message)
        #await Send(websocket, message)
        for sensor in sensors:
            if sensor.isOn and (traffic_light_by_id(sensor.id).state == "green"):
                sensor.isOn = False
        if (not [oldsensors[i].isOn for i in range(0, len(oldsensors))] == [sensors[i].isOn for i in range(0, len(sensors))]):
            message = {
                "msg_id": new_messageid(),
                "msg_type": "notify_sensor_change",
                "data": [{"id": sensor.id, "vehicles_waiting": sensor.isOn, "vehicles_coming": False, "emergency_vehicle": False} for sensor in sensors]
            }

            oldsensors.clear()
            for sensor in sensors:
                newsensor = Sensor(sensor.id)
                newsensor.isOn = sensor.isOn
                oldsensors.append(newsensor)

            await Send(websocket, json.dumps(message))

        if debug:
            print([sensor.isOn for sensor in sensors])

async def Receive(websocket):
    global message_id
    while True:
        try:
            async for jsonmessage in websocket:
                #print(jsonmessage)
                message = json.loads(jsonmessage)
                messages.append(message)
                message_id = message["msg_id"]
                print("-> | MSG #{0}, Type: {1}".format(message_id, message["msg_type"]))
                if message["msg_type"] == "notify_traffic_light_change":
                    for tl in message["data"]:
                        change_traffic_light_state(tl["id"], tl["state"])
        except Exception as ex:
            print("Something went wrong in receiving and/or decoding a message.")
            print(type(ex).__name__, ex.args)
            await asyncio.sleep(1)

async def Send(websocket, message):
    jsonmessage = json.loads(message)
    print("<- | MSG #{0}, Type: {1}".format(jsonmessage["msg_id"], jsonmessage["msg_type"]))
    await websocket.send(message)

def change_traffic_light_state(id, state):
    for i in range(0, len(traffic_lights)):
        if traffic_lights[i].id == id:
            traffic_lights[i].state = state

def traffic_light_by_id(id):
    for tl in traffic_lights:
        if tl.id == id:
            return tl
    return TrafficLight(746, [], 746.0)

def new_messageid():
    global message_id
    message_id = message_id + 1
    return message_id

def initialization():
    traffic_lights.clear()
    crossingsstringlist = ["000000000000000000001111000100010000","000000000000000000000001000100010000","000000000000000000001110000000000000","000000000000000000001110000000000000","000000000000000000000001000100010000","000000000000000000000011101000100000","000000000000000000000010001000100000","000000000000000000000001100000000000","000000000000000000000001100000000000","000000000000000000000010001000100000","000000000000000000000100101111000000","000000000000000000000100100001000000","000000000000000000000000001110000000","000000000000000000000000001110000000","000000000000000000000100100001000000","000000000000000000001001000011110000","000000000000000000001001000010000000","000000000000000000000000000001110000","000000000000000000000000000001110000","000000000000000000001001000010000000","101100000000000110010001001111100000","101100000011001000000001101001100000","101101100100000000000000011000100000","110011011000000110011100011111110000","000001011011001000000100010001000000","000000000000000000000011101000100000","000001100110110000001111010001100000","110010000010110000001001000001110000","000000000010110110011001000000000000","000000000011001101101101101100000000","000001100100000101101111011100000000","110010000000000101100001000100000000","000000000000000000000000000000000110","000000000000000000000000000000001011","000000000000000000000000000000001101","000000000000000000000000000000000110"]
    for tlnr in range(0,36):
        crosses = []
        for x in range(0, len(crossingsstringlist)):
            if crossingsstringlist[tlnr][x] == '1':
                crosses.append(x + 1)
        traffic_lights.append(TrafficLight(tlnr + 1, crosses, 4.0))
    for i in [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25, 26, 27, 28, 31, 32, 33]:
        sensors.append(Sensor(i))
    if debug:
        for sensor in sensors:
            sensor.isOn = True
    message = {
        "msg_id": new_messageid(),
        "msg_type": "initialization",
        "data": [{"id": tl.id, "crosses": tl.crosses, "clearing_time": tl.clearing_time} for tl in traffic_lights]
    }
    return json.dumps(message)

async def register(websocket):
    USERS.add(websocket)
    print("Client with ip: {0}:{1}".format(websocket.remote_address[0], websocket.remote_address[1]), "joined.")

async def unregister(websocket):
    USERS.remove(websocket)

async def counter(websocket, path):
    #starttime = time.time()
    await register(websocket)
    #while True:
    #    await asyncio.sleep(1)
    #    if not websocket.open:
    #        print(time.time() - starttime)
    await Send(websocket, initialization())
    #await Receive(websocket)

    try:
        await asyncio.gather(Receive(websocket), main_loop(websocket))
    except Exception as ex:
        print("Something went wrong while sending the initial message or in the main loop, someone likely disconnected.")
        print(type(ex).__name__, ex.args)
        await asyncio.sleep(1)
    finally:
        await unregister(websocket)

class TrafficLight:
    def __init__(self, id, crosses, clearing_time):
        self.id = id
        self.crosses = crosses
        self.clearing_time = clearing_time
        self.state = "red"

class Sensor:
    def __init__(self, id):
        self.id = id
        self.isOn = False

#wrapper around the even loop's create_server() method. It creates and starts a Server, then it wraps the server in a websocketserver and returns the websocketserver
start_server = websockets.serve(counter, port=6969, ping_interval=None, ping_timeout=None)

asyncio.get_event_loop().run_until_complete(start_server)
asyncio.get_event_loop().run_forever()