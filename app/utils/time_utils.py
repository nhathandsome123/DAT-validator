from datetime import datetime
import pandas as pd


def parse_datetime(value):
    if pd.isna(value):
        return None
    if isinstance(value, datetime):
        return value
    text = str(value).strip()
    if not text:
        return None
    for fmt in ('%d/%m/%Y %H:%M', '%d/%m/%Y %H:%M:%S', '%Y-%m-%d %H:%M:%S'):
        try:
            return datetime.strptime(text, fmt)
        except ValueError:
            pass
    parsed = pd.to_datetime(text, dayfirst=True, errors='coerce')
    if pd.isna(parsed):
        raise ValueError(f'Unable to parse datetime: {value}')
    return parsed.to_pydatetime()
