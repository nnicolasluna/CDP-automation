
import asyncio
import json
import urllib.request
import websockets


class CDPConnection:

    def __init__(self, port=9222):

        self.port = port
        self.ws = None
        self.command_id = 0

    async def connect(self):

        url = f"http://127.0.0.1:{self.port}/json/list"

        for attempt in range(30):

            try:

                with urllib.request.urlopen(url) as response:
                    targets = json.loads(response.read())

                pages = [
                    page for page in targets
                    if page["type"] == "page"
                ]

                if pages:

                    self.ws = await websockets.connect(
                        pages[0]["webSocketDebuggerUrl"]
                    )

                    print("Conectado a Chrome mediante CDP")

                    return

            except Exception:
                pass

            await asyncio.sleep(1)

        raise Exception("No fue posible conectar con Chrome")

    async def send(self, method, params=None):

        self.command_id += 1
        current_id = self.command_id

        await self.ws.send(json.dumps({
            "id": current_id,
            "method": method,
            "params": params or {}
        }))

        while True:

            response = json.loads(await self.ws.recv())

            if response.get("id") == current_id:

                if "error" in response:
                    raise Exception(response["error"])

                return response.get("result", {})

    async def evaluate(self, javascript):

        result = await self.send(
            "Runtime.evaluate",
            {
                "expression": javascript,
                "returnByValue": True,
                "awaitPromise": True
            }
        )

        if "exceptionDetails" in result:
            raise Exception(result["exceptionDetails"])

        return result["result"].get("value")

    async def close(self):

        if self.ws:
            await self.ws.close()
            print("Conexión CDP cerrada")
