from typing import Optional


def to_bool(value: Optional[str]) -> bool:
    return (value or '').lower() in ('1', 'true')
