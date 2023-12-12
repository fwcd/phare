from dataclasses import dataclass
from typing import Any, Generic, Optional, Self, TypeVar

from phare.auth import Auth
from phare.serialize import Deserializable, deserialize, serialize

T = TypeVar("T")
U = TypeVar("U")

@dataclass
class ClientMessage(Generic[T]):
    request_id: int
    verb: str
    path: list[str]
    meta: dict[str, str]
    auth: Auth
    payload: T

    def serialize(self) -> dict[str, Any]:
        return {
            'REID': self.request_id,
            'VERB': self.verb,
            'PATH': self.path,
            'META': self.meta,
            'AUTH': serialize(self.auth),
            'PAYL': serialize(self.payload),
        }

@dataclass
class ServerMessage(Generic[U]):
    code: int
    request_id: Optional[int]
    warnings: list[str]
    response: Optional[str]
    payload: U

    @classmethod
    def deserialize(cls, payload_ty: type[U], raw: dict[str, Any]) -> Self:
        return ServerMessage(
            code=raw['RNUM'],
            request_id=raw.get('REID'),
            warnings=raw.get('WARNINGS', []),
            response=raw.get('RESPONSE'),
            payload=deserialize(payload_ty, raw['PAYL']),
        )

@dataclass
class InputEvent(Deserializable):
    source: int
    key: Optional[int]
    button: Optional[int]
    is_down: bool

    @classmethod
    def from_dict(cls, raw: dict[str, Any]) -> Self:
        return InputEvent(
            source=raw['src'],
            key=raw.get('key'),
            button=raw.get('btn'),
            is_down=raw['dwn'],
        )
