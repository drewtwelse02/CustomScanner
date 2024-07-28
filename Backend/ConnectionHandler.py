import asyncio
from websockets.server import serve

class ConnectionHandler :
    def __init__(self):
        print("Connection Handler Started")
    async def echo(self,websocket):
        async for message in websocket:
            print(message)
    async def setup(self):
        async with serve(self.echo, "localhost", 3001):
            await asyncio.Future()  # run forever

   