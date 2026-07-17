from pathlib import Path
from datetime import datetime
import re


def safe_filename(name: str) -> str:
    return re.sub(r'[^A-Za-z0-9._-]+', '_', Path(name).name)


def report_name_from_upload(filename: str) -> str:
    stem = Path(filename).stem
    safe_stem = re.sub(r'[^A-Za-z0-9._-]+', '_', stem)
    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
    return f'{safe_stem}_report_{timestamp}.xlsx'
