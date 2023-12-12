from dataclasses import dataclass
from typing import Any, Generic, Optional, Self, TypeVar

from phare.auth import Auth
from phare.convert import FromDict, ToDict

T = TypeVar("T", bound=ToDict)
U = TypeVar("U", bound=FromDict)

@dataclass
class ClientMessage(Generic[T], ToDict):
    request_id: int
    verb: str
    path: list[str]
    meta: dict[str, str]
    auth: Auth
    payload: T

    def to_dict(self) -> dict[str, Any]:
        return {
            'REID': self.request_id,
            'VERB': self.verb,
            'PATH': self.path,
            'META': self.meta,
            'AUTH': self.auth,
            'PAYL': self.payload.to_dict(),
        }

@dataclass
class ServerMessage(Generic[U]):
    code: int
    request_id: Optional[int]
    warnings: list[str]
    response: Optional[str]
    payload: U

    @classmethod
    def from_dict(cls, raw: dict[str, Any], payload_type: type[U]) -> Self:
        return ServerMessage(
            code=raw['RNUM'],
            request_id=raw.get('REID'),
            warnings=raw.get('WARNINGS', []),
            response=raw.get('RESPONSE'),
            payload=payload_type.from_dict(raw['PAYL']),
        )

@dataclass
class InputEvent(FromDict):
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
