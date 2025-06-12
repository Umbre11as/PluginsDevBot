from dataclasses import is_dataclass, fields, asdict
from typing import Any, List, Dict, get_type_hints, get_origin, get_args
from datetime import datetime, date
from enum import Enum

from ..core.base import Serializer

class SerializationError(Exception):
    pass

class BaseSerializer(Serializer):
    def serialize(self, obj: Any) -> Any:
        return self._serialize_value(obj)

    def _serialize_value(self, value: Any) -> Any:
        if value is None:
            return None
        elif isinstance(value, (str, int, float, bool)):
            return value
        elif isinstance(value, (datetime, date)):
            return value.isoformat()
        elif isinstance(value, Enum):
            return value.value
        elif isinstance(value, dict):
            return {k: self._serialize_value(v) for k, v in value.items()}
        elif isinstance(value, (list, tuple, set)):
            return [self._serialize_value(item) for item in value]
        elif is_dataclass(value):
            return self._serialize_dataclass(value)
        else:
            return self._serialize_object(value)

    def _serialize_dataclass(self, obj: Any) -> Dict[str, Any]:
        result = {}
        for field in fields(obj):
            value = getattr(obj, field.name)
            result[field.name] = self._serialize_value(value)
        return result

    def _serialize_object(self, obj: Any) -> Any:
        if hasattr(obj, '__dict__'):
            return {k: self._serialize_value(v) for k, v in obj.__dict__.items()
                    if not k.startswith('_')}
        else:
            raise SerializationError(f'Cannot serialize object of type {type(obj)}')
