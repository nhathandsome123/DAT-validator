from pathlib import Path
import logging
from logging.handlers import RotatingFileHandler

from fastapi import FastAPI, Request, UploadFile, File, HTTPException
from fastapi.responses import HTMLResponse, FileResponse, JSONResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates

from app.config import LOG_DIR, OUTPUT_DIR, UPLOAD_DIR
from app.core.engine import process_files
from app.utils.file_utils import report_name_from_upload, safe_filename

app = FastAPI(title='DAT Validator')
app.mount('/static', StaticFiles(directory='app/static'), name='static')
templates = Jinja2Templates(directory='app/templates')

handler = RotatingFileHandler(LOG_DIR / 'app.log', maxBytes=1_000_000, backupCount=3, encoding='utf-8')
logging.basicConfig(level=logging.INFO, handlers=[handler])


@app.get('/', response_class=HTMLResponse)
def home(request: Request):
    return templates.TemplateResponse('index.html', {'request': request})


@app.post('/process')
async def process(dat_file: UploadFile = File(...), assignment_file: UploadFile = File(...)):
    if not dat_file.filename.lower().endswith('.xls'):
        raise HTTPException(status_code=400, detail='DAT file must be .xls')
    if not assignment_file.filename.lower().endswith('.xlsx'):
        raise HTTPException(status_code=400, detail='Assignment file must be .xlsx')

    dat_path = UPLOAD_DIR / safe_filename(dat_file.filename)
    assignment_path = UPLOAD_DIR / safe_filename(assignment_file.filename)
    dat_path.write_bytes(await dat_file.read())
    assignment_path.write_bytes(await assignment_file.read())

    report_name = report_name_from_upload(dat_file.filename)
    output_path = OUTPUT_DIR / report_name

    try:
        result = process_files(dat_path, assignment_path, output_path)
        result['download_url'] = f'/download/{report_name}'
        return JSONResponse(result)
    except Exception as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc
    finally:
        for path in [dat_path, assignment_path]:
            try:
                path.unlink(missing_ok=True)
            except Exception:
                pass


@app.get('/download/{filename}')
def download(filename: str):
    path = OUTPUT_DIR / Path(filename).name
    if not path.exists():
        raise HTTPException(status_code=404, detail='Report not found')
    return FileResponse(path, filename=path.name, media_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
