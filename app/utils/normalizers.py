import re
from typing import Any


def _to_text(value: Any) -> str:
    if value is None:
        return ''
    text = str(value)
    if text.lower() == 'nan':
        return ''
    return text


def normalize_text(value: Any) -> str:
    return ' '.join(_to_text(value).strip().split())


def normalize_name(value: Any) -> str:
    return normalize_text(value).lower()


def normalize_student_id(value: Any) -> str:
    return normalize_text(value).upper()


def normalize_plate(value: Any) -> str:
    text = normalize_text(value).upper()
    return re.sub(r'[^A-Z0-9]', '', text)
