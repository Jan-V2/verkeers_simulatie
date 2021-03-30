import asyncio
import websockets

async def hello(websocket, path):
    name = await websocket.recv()
    print(f"<{name}")

    greeting = f"Hello {name}!"

    await websocket.send(greeting)

#wrapper around the even loop's create_server() method. It creates and starts a Server, then it wraps the server in a websocketserver and returns the websocketserver
start_server = websockets.serve(hello, port=6969)

asyncio.get_event_loop().run_until_complete(start_server)
asyncio.get_event_loop().run_forever()