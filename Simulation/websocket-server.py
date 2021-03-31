import asyncio
import websockets
import json
import logging

logging.basicConfig()

STATE = {"value": 0}

USERS = set()

def state_event():
    #Dumps is used to write a Python object into a JSON string
    return json.dumps({"type": "state", **STATE})

def users_event():
    return json.dumps({"type": "users", "count": len(USERS)})

async def notify_state():
    if USERS: #asyncio.wait doesn't accept an empty list
        message = state_event()
        await asyncio.wait([user.send(message) for user in USERS])

async def notify_users():
    if USERS:
        message = users_event()
        await asyncio.wait([user.send(message) for user in USERS])

async def register(websocket):
    USERS.add(websocket)
    await notify_users()

async def unregister(websocket):
    USERS.remove(websocket)
    await notify_users()

async def counter(websocket, path):
    #register(websocket) sends user_event() to websocket
    await register(websocket)
    try:
        await websocket.send(state_event())
        async for message in websocket:
            data = json.loads(message)
            #if data["action"] == "minus":
                #STATE["value"] -= 1
                #await notify_state()
            #elif data["action"] == "plus":
                #STATE["value"] += 1
                #await notify_state()
            #else:
                #logging.error("unsupported event: {} ", data)
    finally:
        await unregister(websocket)

#wrapper around the even loop's create_server() method. It creates and starts a Server, then it wraps the server in a websocketserver and returns the websocketserver
start_server = websockets.serve(counter, port=6969)

asyncio.get_event_loop().run_until_complete(start_server)
asyncio.get_event_loop().run_forever()