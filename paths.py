from pathlib import Path
import sys

# Base folder of the application
if getattr(sys, "frozen", False):
    BASE_DIR = Path(sys.executable).parent
else:
    BASE_DIR = Path(__file__).resolve().parent

DATA_DIR = BASE_DIR / "Data"
OUTPUTS_DIR = BASE_DIR / "Outputs"
OCR_DIR = BASE_DIR / "OCR"
PARSERS_DIR = BASE_DIR / "Parsers"
DOCS_DIR = BASE_DIR / "Docs"

# Tesseract / Poppler: prefer a copy bundled next to the app (drop a
# "Tesseract-OCR" folder and a "poppler" folder beside gui.exe for a
# release build), otherwise fall back to the fixed dev-machine install
# location so this still works when running "python gui.py" directly.
_BUNDLED_TESSERACT = BASE_DIR / "Tesseract-OCR" / "tesseract.exe"
_BUNDLED_POPPLER = BASE_DIR / "poppler" / "Library" / "bin"

TESSERACT_CMD = (
    str(_BUNDLED_TESSERACT) if _BUNDLED_TESSERACT.exists()
    else r"C:\Program Files\Tesseract-OCR\tesseract.exe"
)

POPPLER_PATH = (
    str(_BUNDLED_POPPLER) if _BUNDLED_POPPLER.exists()
    else r"C:\poppler\poppler-26.02.0\Library\bin"
)
