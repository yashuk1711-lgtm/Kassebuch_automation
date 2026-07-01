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