from OCR.pdf_to_words import pdf_to_words
from OCR.row_builder import build_rows

import paths
import config

from Parsers import export_pos_csv
from Parsers import parse_nexi
from Parsers import parse_lieferando
from Parsers import export_lieferando_cash
from Parsers import export_lieferando_tips
from Parsers import export_uber_csv
from Parsers import generate_full_kassenbuch

import pandas as pd


MONTH_NUMBERS = {
    "January": "01",
    "February": "02",
    "March": "03",
    "April": "04",
    "May": "05",
    "June": "06",
    "July": "07",
    "August": "08",
    "September": "09",
    "October": "10",
    "November": "11",
    "December": "12"
}

MONTH_ORDER = list(MONTH_NUMBERS.keys())

# Steps are run in-process (not via subprocess) so this works both as
# "python gui.py" and inside a frozen PyInstaller build, where
# sys.executable points at the packaged EXE itself rather than a real
# Python interpreter.
STEPS = [
    ("POS Export", export_pos_csv),
    ("NEXI Export", parse_nexi),
    ("Lieferando Bank", parse_lieferando),
    ("Lieferando Cash", export_lieferando_cash),
    ("Lieferando Tips", export_lieferando_tips),
    ("Uber Export", export_uber_csv),
    ("Generate Kassenbuch", generate_full_kassenbuch)
]


def _resolve_starting_balance(month, manual_starting_balance):

    month_index = MONTH_ORDER.index(month)

    if month_index > 0:

        prev_month = MONTH_ORDER[month_index - 1]
        prev_file = paths.OUTPUTS_DIR / f"{prev_month.lower()}_kassenbuch_full.csv"

        if prev_file.exists():
            prev_df = pd.read_csv(prev_file)
            return round(float(prev_df.iloc[-1]["Neuestand"]), 2)

    if manual_starting_balance is not None:
        return manual_starting_balance

    raise ValueError(
        f"No previous month's Kassenbuch was found and no starting "
        f"balance was entered. Enter a starting balance for {month} "
        f"in the field above."
    )


def run_automation(
    month,
    starting_balance=None,
    progress_callback=None,
    status_callback=None
):
    """
    Runs the complete automation in-process.
    """

    # -----------------------------------------
    # Store selected month + starting balance
    # -----------------------------------------

    month_num = MONTH_NUMBERS[month]
    resolved_balance = _resolve_starting_balance(month, starting_balance)

    config.set_month(month, month_num, resolved_balance)

    # -----------------------------------------
    # OCR Bank Statement
    # -----------------------------------------

    bank_pdf = paths.DATA_DIR / "Bank" / f"{month}_Bank_Statement.pdf"

    if not bank_pdf.exists():
        raise FileNotFoundError(
            f"Bank statement not found:\n{bank_pdf}"
        )

    paths.OUTPUTS_DIR.mkdir(parents=True, exist_ok=True)

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

    total = len(STEPS)

    for i, (name, module) in enumerate(STEPS):

        if status_callback:
            status_callback(name)

        print(f"\nRunning: {name}")

        module.run()

        if progress_callback:
            progress_callback((i + 1) / total)

    return True
