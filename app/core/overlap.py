from collections import defaultdict
from typing import Dict, List

from app.core.parser import SessionRecord
from app.core.rules import Finding


def detect_overlaps(sessions: List[SessionRecord]) -> Dict[str, List[Finding]]:
    by_student = defaultdict(list)
    for session in sessions:
        by_student[session.student_id].append(session)

    overlap_findings: Dict[str, List[Finding]] = defaultdict(list)
    for _, student_sessions in by_student.items():
        ordered = sorted(student_sessions, key=lambda s: s.start_time)
        for prev, curr in zip(ordered, ordered[1:]):
            if prev.end_time > curr.start_time:
                msg_curr = f'Overlap detected with session {prev.session_id} ({prev.start_time:%d/%m/%Y %H:%M} - {prev.end_time:%d/%m/%Y %H:%M})'
                msg_prev = f'Overlap detected with session {curr.session_id} ({curr.start_time:%d/%m/%Y %H:%M} - {curr.end_time:%d/%m/%Y %H:%M})'
                overlap_findings[curr.session_id].append(Finding('session_overlap', 'ERROR', msg_curr))
                overlap_findings[prev.session_id].append(Finding('session_overlap', 'ERROR', msg_prev))
    return overlap_findings
