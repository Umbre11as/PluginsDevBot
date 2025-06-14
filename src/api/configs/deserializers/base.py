from dataclasses import is_dataclass, fields
from typing import Any, Type, List, Dict, get_type_hints, get_origin, get_args, Union
from datetime import datetime, date
from enum import Enum

from ..core.base import Deserializer

class ValidationError(Exception):
    pass

class DeserializationError(Exception):
    pass

class BaseDeserializer(Deserializer):
    def deserialize(self, cls: Type[Any], data: Any) -> Any:
        if is_dataclass(cls):
            return self._deserialize_dataclass(cls, data)
        else:
            return self._deserialize_type(cls, data)

    def _deserialize_type(self, cls: Type[Any], value: Any) -> Any:
        if value is None:
            return None

        origin = get_origin(cls)
        if origin is Union:
            args = get_args(cls)
            if len(args) == 2 and type(None) in args:
                other_type = args[0] if args[1] is type(None) else args[1]
                return self._deserialize_type(other_type, value) if value is not None else None
            else:
                for arg_type in args:
                    try:
                        return self._deserialize_type(arg_type, value)
                    except:
                        continue
                raise DeserializationError(f'Cannot deserialize {value} to Union{args}')

        if origin is list or cls is list:
            if not isinstance(value, list):
                raise ValidationError(f'Expected list, got {type(value)}')
            item_type = get_args(cls)[0] if get_args(cls) else Any
            return [self._deserialize_type(item_type, item) for item in value]

        if origin is dict or cls is dict:
            if not isinstance(value, dict):
                raise ValidationError(f'Expected dict, got {type(value)}')
            if get_args(cls):
                key_type, value_type = get_args(cls)
                return {self._deserialize_type(key_type, k): self._deserialize_type(value_type, v) 
                        for k, v in value.items()}
            return value

        if cls in (str, int, float, bool):
            if not isinstance(value, cls):
                try:
                    return cls(value)
                except:
                    raise ValidationError(f'Cannot convert {value} to {cls}')
            return value

        if cls is datetime:
            if isinstance(value, str):
                return datetime.fromisoformat(value)
            elif isinstance(value, datetime):
                return value
            else:
                raise ValidationError(f'Cannot convert {value} to datetime')

        if cls is date:
            if isinstance(value, str):
                return date.fromisoformat(value)
            elif isinstance(value, date):
                return value
            else:
                raise ValidationError(f'Cannot convert {value} to date')

        if isinstance(cls, type) and issubclass(cls, Enum):
            if isinstance(value, str):
                for member in cls:
                    if member.value == value:
                        return member
                raise ValidationError(f'Invalid enum value: {value}')
            return value

        if is_dataclass(cls):
            return self._deserialize_dataclass(cls, value)

        if hasattr(cls, '__init__'):
            return cls(**value) if isinstance(value, dict) else cls(value)

        return value

    def _deserialize_dataclass(self, cls: Type[Any], data: Dict[str, Any]) -> Any:
        if not isinstance(data, dict):
            raise ValidationError(f'Expected dict for dataclass {cls.__name__}, got {type(data)}')

        type_hints = get_type_hints(cls)
        init_kwargs = {}

        for field in fields(cls):
            field_name = field.name
            field_type = type_hints.get(field_name, field.type)
            
            if field_name in data:
                value = data[field_name]
                init_kwargs[field_name] = self._deserialize_type(field_type, value)
            elif field.default is not field.default_factory:
                init_kwargs[field_name] = field.default
            elif field.default_factory is not field.default_factory:
                init_kwargs[field_name] = field.default_factory()
            else:
                raise ValidationError(f'Missing required field: {field_name}')

        return cls(**init_kwargs)
