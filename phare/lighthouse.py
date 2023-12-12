from numpy.typing import ArrayLike
from typing import Any, Self, TypeVar

from phare.auth import Auth
from phare.constants import LIGHTHOUSE_FRAME_SHAPE, LIGHTHOUSE_URL
from phare.serialize import serialize
from phare.protocol import ClientMessage

import msgpack
import numpy as np
import websockets

T = TypeVar("T")

class Lighthouse:
    def __init__(self, auth: Auth, websocket: websockets.WebSocketClientProtocol):
        self.auth = auth
        self.websocket = websocket
        self.request_id = 0
    
    @classmethod
    async def connect(cls, auth: Auth, url: str = LIGHTHOUSE_URL) -> Self:
        websocket = await websockets.connect(url)
        return Lighthouse(
            auth=auth,
            websocket=websocket,
        )

    async def __aenter__(self):
        return self
    
    async def __aexit__(self, _exc_type: Any, _exc_value: Any, _exc_traceback: Any):
        await self.websocket.close()
        

    async def put_model(self, frame: ArrayLike):
        frame = np.asarray(frame)
        assert frame.shape == LIGHTHOUSE_FRAME_SHAPE
        assert frame.dtype == np.uint8
        await self.put(['user', self.auth.user, 'model'], frame)
        # TODO: Return response

    async def put(self, path: list[str], payload: Any):
        await self.perform('PUT', path, payload)
        # TODO: Return response

    async def perform(self, verb: str, path: list[str], payload: Any):
        assert verb != 'STREAM'
        await self.send_request(verb, path, payload)
        # TODO: Receive response and return it

    async def send_request(self, verb: str, path: list[str], payload: Any):
        request_id = self.request_id
        self.request_id += 1
        await self.send_message(ClientMessage(
            request_id=request_id,
            verb=verb,
            path=path,
            meta={},
            auth=self.auth,
            payload=payload,
        ))

    async def send_message(self, message: ClientMessage[Any]):
        binary: bytes = msgpack.packb(serialize(message))
        await self.websocket.send(binary)
