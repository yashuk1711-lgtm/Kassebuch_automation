from OCR.pdf_to_words import pdf_to_words
from OCR.row_builder import build_rows

from paths import DATA_DIR

import subprocess
import json
import sys
import config


MONTHS = {
    "January": "January",
    "February": "February",
    "March": "March",
    "April": "April",
    "May": "May",
    "June": "June",
    "July": "July",
    "August": "August",
    "September": "September",
    "October": "October",
    "November": "November",
    "December": "December"
}


scripts = [
    ("POS Export", "Parsers/export_pos_csv.py"),
    ("Parse NEXI", "Parsers/parse_nexi.py"),
    ("Parse Lieferando", "Parsers/parse_lieferando.py"),
    ("Lieferando Cash", "Parsers/export_lieferando_cash.py"),
    ("Lieferando Tips", "Parsers/export_lieferando_tips.py"),
    ("Uber Export", "Parsers/export_uber_csv.py"),
    ("Generate Kassenbuch", "Parsers/generate_full_kassenbuch.py")
]


def run_automation(month, progress_callback=None, status_callback=None):
    """
    Runs the complete automation.
    """

    # -----------------------------------------
    # Store selected month
    # -----------------------------------------

    config.MONTH = month
    config.MONTH_LOWER = month.lower()

    settings = {
        "month": config.MONTH,
        "month_lower": config.MONTH_LOWER
    }

    with open("selected_month.json", "w") as f:
        json.dump(settings, f, indent=4)

    # -----------------------------------------
    # OCR Bank Statement
    # -----------------------------------------

    bank_pdf = DATA_DIR / "Bank" / f"{month}_Bank_Statement.pdf"

    if not bank_pdf.exists():
        raise FileNotFoundError(
            f"Bank statement not found:\n{bank_pdf}"
        )

    print("=" * 60)
    print("Generating OCR Words...")
    print("=" * 60)

    pdf_to_words(str(bank_pdf))

    print("=" * 60)
    print("Building OCR Rows...")
    print("=" * 60)

    build_rows()

    # -----------------------------------------
    # Run remaining parsers
    # -----------------------------------------

    total = len(scripts)

    for i, (name, script) in enumerate(scripts):

        if status_callback:
            status_callback(name)

        print(f"\nRunning: {name}")

        result = subprocess.run(
            [sys.executable, script],
            text=True
        )

        if result.returncode != 0:
            raise Exception(f"{name} failed.")

        if progress_callback:
            progress_callback((i + 1) / total)

    return True