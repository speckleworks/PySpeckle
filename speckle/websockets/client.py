import asyncio
import websockets


async def hello():
    async with websockets.connect(
            'wss://hestia.speckle.works/') as websocket:
        name = input("What's your name? ")

        await websocket.send(name)
        print(f"> {name}")

        greeting = await websocket.recv()
        print(f"< {greeting}")

asyncio.get_event_loop().run_until_complete(hello())

# websockets.client.