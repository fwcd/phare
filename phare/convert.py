from typing import Any, Protocol, Self

class ToDict(Protocol):
    def to_dict(self) -> dict[str, Any]:
        raise NotImplementedError(f'to_dict is not implemented for {type(self).__name__}')
    
class FromDict(Protocol):
    @classmethod
    def from_dict(cls, raw: dict[str, Any]) -> Self:
        raise NotImplementedError(f'from_dict is not implemented for {cls.__name__}')
