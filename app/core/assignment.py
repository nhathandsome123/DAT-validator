from dataclasses import dataclass
from pathlib import Path
from typing import Dict
import pandas as pd

from app.utils.normalizers import normalize_name, normalize_plate, normalize_student_id, normalize_text


@dataclass
class AssignmentRecord:
    student_id: str
    student_name_raw: str
    teacher_raw: str
    vehicle_raw: str
    teacher_norm: str
    vehicle_norm: str


def load_assignment_map(path: str | Path) -> Dict[str, AssignmentRecord]:
    df = pd.read_excel(path)
    required = ['Mã học viên', 'Họ & Tên', 'Phân Giáo Viên', 'Biển số xe']
    missing = [col for col in required if col not in df.columns]
    if missing:
        raise ValueError(f'Missing required assignment columns: {missing}')

    mapping = {}
    duplicates = []
    for _, row in df.iterrows():
        student_id = normalize_student_id(row['Mã học viên'])
        if not student_id:
            continue
        record = AssignmentRecord(
            student_id=student_id,
            student_name_raw=normalize_text(row['Họ & Tên']),
            teacher_raw=normalize_text(row['Phân Giáo Viên']),
            vehicle_raw=normalize_text(row['Biển số xe']),
            teacher_norm=normalize_name(row['Phân Giáo Viên']),
            vehicle_norm=normalize_plate(row['Biển số xe']),
        )
        if student_id in mapping:
            duplicates.append(student_id)
        mapping[student_id] = record
    if duplicates:
        raise ValueError(f'Duplicate student IDs found in assignment file: {sorted(set(duplicates))[:10]}')
    return mapping
