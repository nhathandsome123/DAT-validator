from dataclasses import dataclass
from pathlib import Path
import subprocess
import tempfile
import shutil
from typing import List

import pandas as pd

from app.utils.normalizers import normalize_name, normalize_plate, normalize_student_id, normalize_text
from app.utils.time_utils import parse_datetime

HEADER_ROW_INDEX = 3
COLUMN_MAP = {
    'STT': 'row_no',
    'Mã phiên học': 'session_id',
    'Tỉ lệ nhận diện': 'recognition',
    'Thời gian bắt đầu phiên học': 'start_time',
    'Thời gian kết thúc phiên học': 'end_time',
    'Thời gian thực hành (giờ) (CSĐT truyền lên)': 'duration_hours',
    'Quãng đường thực hành (km) (CSĐT truyền lên)': 'distance_km',
    'Thời gian máy chủ nhận phiên học': 'server_time',
    'Mã học viên': 'student_id',
    'Họ và tên học viên': 'student_name',
    'Mã Khóa học': 'course_code',
    'Tên Khóa học': 'class_name',
    'Loại Khóa học': 'license_type',
    'Họ và tên giáo viên': 'teacher_name',
    'Mã giáo viên': 'teacher_id',
    'Biển số Xe': 'vehicle_plate',
    'Sở GTVT quản lý': 'authority',
    'Cơ sở đào tạo': 'training_center',
}


@dataclass
class SessionRecord:
    source_row_number: int
    row_no: int
    session_id: str
    recognition: int
    start_time: object
    end_time: object
    duration_hours: float
    distance_km: float
    student_id: str
    student_name_raw: str
    teacher_name_raw: str
    vehicle_plate_raw: str
    student_name_norm: str
    teacher_name_norm: str
    vehicle_plate_norm: str
    raw: dict

    @property
    def speed_kmh(self) -> float:
        if not self.duration_hours:
            return 0.0
        return float(self.distance_km) / float(self.duration_hours)


def _read_xls_with_fallback(path: str | Path) -> pd.DataFrame:
    try:
        return pd.read_excel(path, header=HEADER_ROW_INDEX)
    except ImportError:
        soffice = shutil.which('libreoffice') or shutil.which('soffice')
        if not soffice:
            raise
        with tempfile.TemporaryDirectory() as tmpdir:
            profile_dir = Path(tmpdir) / 'lo-profile'
            profile_dir.mkdir(parents=True, exist_ok=True)
            subprocess.run([
                soffice,
                f'-env:UserInstallation=file://{profile_dir}',
                '--headless',
                '--convert-to', 'xlsx',
                '--outdir', tmpdir,
                str(path),
            ], check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            converted = Path(tmpdir) / f'{Path(path).stem}.xlsx'
            return pd.read_excel(converted, header=HEADER_ROW_INDEX)


def load_dat_sessions(path: str | Path) -> List[SessionRecord]:
    df = _read_xls_with_fallback(path)
    missing = [col for col in COLUMN_MAP if col not in df.columns]
    if missing:
        raise ValueError(f'Missing required DAT columns: {missing}')

    records = []
    for idx, row in df.iterrows():
        raw = {COLUMN_MAP[col]: row[col] for col in COLUMN_MAP}
        student_name_raw = normalize_text(raw['student_name'])
        teacher_name_raw = normalize_text(raw['teacher_name'])
        vehicle_plate_raw = normalize_text(raw['vehicle_plate'])
        records.append(SessionRecord(
            source_row_number=int(idx) + HEADER_ROW_INDEX + 2,
            row_no=int(raw['row_no']),
            session_id=normalize_text(raw['session_id']),
            recognition=int(raw['recognition']),
            start_time=parse_datetime(raw['start_time']),
            end_time=parse_datetime(raw['end_time']),
            duration_hours=float(raw['duration_hours']),
            distance_km=float(raw['distance_km']),
            student_id=normalize_student_id(raw['student_id']),
            student_name_raw=student_name_raw,
            teacher_name_raw=teacher_name_raw,
            vehicle_plate_raw=vehicle_plate_raw,
            student_name_norm=normalize_name(student_name_raw),
            teacher_name_norm=normalize_name(teacher_name_raw),
            vehicle_plate_norm=normalize_plate(vehicle_plate_raw),
            raw=raw,
        ))
    return records
