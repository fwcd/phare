from dataclasses import dataclass
from typing import Generic, Optional, TypeVar

from phare.auth import Auth

T = TypeVar("T")

@dataclass
class ClientMessage(Generic[T]):
    request_id: int
    verb: str
    path: list[str]
    meta: dict[str, str]
    auth: Auth
    payload: T

@dataclass
class ServerMessage(Generic[T]):
    code: int
    request_id: Optional[int]
    warnings: list[str]
    response: Optional[str]
    payload: T

@dataclass
class InputEvent:
    source: int
    key: Optional[int]
    button: Optional[int]
    is_down: bool
