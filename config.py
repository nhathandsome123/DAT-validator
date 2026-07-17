from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent
DATA_DIR = BASE_DIR / 'data'
UPLOAD_DIR = DATA_DIR / 'uploads'
OUTPUT_DIR = DATA_DIR / 'output'
LOG_DIR = DATA_DIR / 'logs'
RULESET_PATH = BASE_DIR / 'rulesets' / 'default_rules.json'

for path in [UPLOAD_DIR, OUTPUT_DIR, LOG_DIR]:
    path.mkdir(parents=True, exist_ok=True)
