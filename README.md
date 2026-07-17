# DAT Validator

Local Docker web app for checking DAT session files against hard-coded anomaly rules.

## Features
- Upload one DAT `.xls` file and one assignment `.xlsx` file
- Checks recognition, speed, distance, duration, teacher assignment, vehicle assignment, and session overlap
- Generates an Excel report with Summary, Findings, Full Data, and Evening Summary sheets
- Highlights `ERROR` rows in red and `WARNING` rows in yellow
- Evening Summary calculates each student's valid evening riding time from 18:00 to 00:00
- Sessions with any `ERROR` are excluded from the evening total

## Run with Docker
```bash
docker compose up --build
```

Then open `http://localhost:8000`.

## Expected assignment columns
- `Mã học viên`
- `Họ & Tên`
- `Phân Giáo Viên`
- `Biển số xe`

## Rules in v1
- Recognition `< 75` => ERROR
- Recognition `75–79` => WARNING
- Speed `< 25 km/h` => WARNING
- Distance `< 5 km` => ERROR
- Duration `< 10 minutes` => ERROR
- Teacher mismatch => ERROR
- Vehicle mismatch => ERROR
- Session overlap => ERROR
