from dataclasses import dataclass
from typing import List, Optional

from app.core.assignment import AssignmentRecord
from app.core.parser import SessionRecord


@dataclass
class Finding:
    rule: str
    severity: str
    message: str
    value: Optional[str] = None


MIN_RECOGNITION_ERROR = 75
MIN_RECOGNITION_WARNING = 80
MIN_SPEED_WARNING = 25
MIN_DISTANCE_ERROR = 5
MIN_DURATION_ERROR_HOURS = 10 / 60


def evaluate_session(session: SessionRecord, assignment: Optional[AssignmentRecord]) -> List[Finding]:
    findings: List[Finding] = []

    if session.recognition < MIN_RECOGNITION_ERROR:
        findings.append(Finding('recognition', 'ERROR', 'Face recognition below 75', str(session.recognition)))
    elif MIN_RECOGNITION_ERROR <= session.recognition < MIN_RECOGNITION_WARNING:
        findings.append(Finding('recognition', 'WARNING', 'Face recognition is borderline (75-79)', str(session.recognition)))

    if session.speed_kmh < MIN_SPEED_WARNING:
        findings.append(Finding('speed', 'WARNING', 'Average speed below 25 km/h', f'{session.speed_kmh:.2f}'))

    if session.distance_km < MIN_DISTANCE_ERROR:
        findings.append(Finding('distance', 'ERROR', 'Distance below 5 km', f'{session.distance_km:.2f}'))

    if session.duration_hours < MIN_DURATION_ERROR_HOURS:
        findings.append(Finding('duration', 'ERROR', 'Duration below 10 minutes', f'{session.duration_hours:.2f}'))

    if assignment is None:
        findings.append(Finding('assignment_missing', 'WARNING', 'Student ID not found in assignment file', session.student_id))
        return findings

    if session.teacher_name_norm != assignment.teacher_norm:
        findings.append(Finding('teacher_mismatch', 'ERROR', 'Teacher does not match assignment', f'DAT={session.teacher_name_raw} | Assignment={assignment.teacher_raw}'))

    if session.vehicle_plate_norm != assignment.vehicle_norm:
        findings.append(Finding('vehicle_mismatch', 'ERROR', 'Vehicle does not match assignment', f'DAT={session.vehicle_plate_raw} | Assignment={assignment.vehicle_raw}'))

    return findings
