from typing import Any, Self, TypeVar

from phare.auth import Auth
from phare.constants import LIGHTHOUSE_URL
from phare.convert import ToDict
from phare.protocol import ClientMessage

import msgpack # type: ignore
import websockets

T = TypeVar("T")

class Lighthouse:
    def __init__(self, auth: Auth, websocket: websockets.WebSocketClientProtocol):
        self.auth = auth
        self.websocket = websocket
    
    @classmethod
    async def connect(cls, auth: Auth, url: str = LIGHTHOUSE_URL) -> Self:
        websocket = await websockets.connect(url)
        return Lighthouse(
            auth=auth,
            websocket=websocket,
        )

    def __enter__(self):
        return self
    
    async def __exit__(self, _exc_type: Any, _exc_value: Any, _exc_traceback: Any):
        await self.websocket.close()

    async def send_message(self, message: ClientMessage[ToDict]):
        binary: bytes = msgpack.packb(message) # type: ignore
        await self.websocket.send(binary)
