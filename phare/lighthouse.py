from typing import TypeVar
from websocket import create_connection # type: ignore

from phare.auth import Auth
from phare.constants import LIGHTHOUSE_URL
from phare.convert import ToDict
from phare.protocol import ClientMessage

T = TypeVar("T")

class Lighthouse:
    def __init__(self, auth: Auth, url: str = LIGHTHOUSE_URL):
        self.auth = auth
        self.websocket = create_connection(url)
    
    def send_message(self, message: ClientMessage[ToDict]):
        pass
