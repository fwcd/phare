from typing import Any, Protocol, Self, TypeVar

from phare.error import DeserializeError

T = TypeVar("T")

class Serializable(Protocol):
    def serialize(self) -> dict[str, Any]:
        raise NotImplementedError(f'serialize is not implemented for {type(self).__name__}')
    
class Deserializable(Protocol):
    @classmethod
    def deserialize(cls, raw: dict[str, Any]) -> Self:
        raise NotImplementedError(f'deserialize is not implemented for {cls.__name__}')

def serialize(value: Any) -> Any:
    '''
    Converts the argument to a 'JSON-style' representation, i.e. dictionaries,
    arrays and primitives. This conversion is made on a best-effort basis and
    will default to returning any unrecognized values verbatim.
    '''

    if (serialize := getattr(value, 'serialize')) and callable(serialize):
        return serialize(value)
    else:
        return value

def deserialize(ty: type[T], raw: Any) -> T:
    '''
    Converts the argument from a 'JSON-style' representation to the given type.
    Will throw `DeserializeError` if the conversion failed.
    '''

    if (deserialize := getattr(ty, 'deserialize')) and callable(deserialize):
        value = deserialize(ty, raw)
    else:
        value = raw
    if not isinstance(value, ty):
        raise DeserializeError(f'Could not deserialize {raw} to {ty}')
    return value
