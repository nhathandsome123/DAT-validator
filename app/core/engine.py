import json
import logging
import time
from pathlib import Path
from typing import Dict, Any

from app.core.assignment import load_assignment_map
from app.core.overlap import detect_overlaps
from app.core.parser import load_dat_sessions
from app.core.rules import evaluate_session, Finding
from app.reporting.excel_report import build_report

logger = logging.getLogger(__name__)


def process_files(dat_path: str | Path, assignment_path: str | Path, output_path: str | Path) -> Dict[str, Any]:
    start = time.perf_counter()
    sessions = load_dat_sessions(dat_path)
    assignment_map = load_assignment_map(assignment_path)

    findings_by_session: Dict[str, list[Finding]] = {}
    for session in sessions:
        findings_by_session[session.session_id] = evaluate_session(session, assignment_map.get(session.student_id))

    overlap_findings = detect_overlaps(sessions)
    for session_id, overlap_list in overlap_findings.items():
        findings_by_session.setdefault(session_id, []).extend(overlap_list)

    build_report(output_path, sessions, findings_by_session)

    error_count = sum(1 for findings in findings_by_session.values() for f in findings if f.severity == 'ERROR')
    warning_count = sum(1 for findings in findings_by_session.values() for f in findings if f.severity == 'WARNING')
    elapsed = round(time.perf_counter() - start, 2)

    result = {
        'total_sessions': len(sessions),
        'error_count': error_count,
        'warning_count': warning_count,
        'elapsed_seconds': elapsed,
        'output_path': str(output_path),
    }
    logger.info(json.dumps(result))
    return result
