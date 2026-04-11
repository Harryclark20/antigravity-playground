import asyncio
import websockets
import json
import threading
import queue

class Broadcaster:
    def __init__(self, host="127.0.0.1", port=8765):
        self.host = host
        self.port = port
        self.queue = queue.Queue()
        self.clients = set()
        self.loop = None
        self.thread = threading.Thread(target=self._start_event_loop, daemon=True)
        self.thread.start()

    def _start_event_loop(self):
        """Starts the background asyncio event loop."""
        self.loop = asyncio.new_event_loop()
        asyncio.set_event_loop(self.loop)
        
        start_server = websockets.serve(self._handler, self.host, self.port)
        self.loop.run_until_complete(start_server)
        print(f"WebSocket Broadcaster started on ws://{self.host}:{self.port}")
        self.loop.run_forever()

    async def _handler(self, websocket, path):
        """Handles new UI client connections."""
        self.clients.add(websocket)
        try:
            async for message in websocket:
                # Handle potential incoming commands from UI (like Kill Switch)
                data = json.loads(message)
                if data.get("command") == "KILL_SWITCH":
                    print("!!! UI KILL SWITCH TRIGGERED !!!")
                    # Here we would trigger the global halt
        finally:
            self.clients.remove(websocket)

    def broadcast(self, data):
        """
        Public method to fire a JSON packet. 
        Thread-safe and Non-blocking for the MT5 loop.
        """
        if self.loop and self.clients:
            asyncio.run_coroutine_threadsafe(self._send_to_all(data), self.loop)

    async def _send_to_all(self, data):
        """Internal helper to broadcast to all connected UI clients."""
        if not self.clients:
            return
            
        message = json.dumps(data)
        # Create a list to avoid 'Set changed size during iteration' errors
        for client in list(self.clients):
            try:
                await client.send(message)
            except websockets.exceptions.ConnectionClosed:
                self.clients.remove(client)
