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
    ("NEXI Export", "Parsers/export_nexi_csv.py"),
    ("Lieferando Bank", "Parsers/export_lieferando_csv.py"),
    ("Lieferando Cash", "Parsers/export_lieferando_cash.py"),
    ("Lieferando Tips", "Parsers/export_lieferando_tips.py"),
    ("Uber Export", "Parsers/export_uber_csv.py"),
    ("Generate Kassenbuch", "Parsers/generate_full_kassenbuch.py")
]


def run_automation(month, progress_callback=None, status_callback=None):
    """
    Runs the complete automation.
    """

    config.MONTH = month
    config.MONTH_LOWER = month.lower()

    settings = {
        "month": config.MONTH,
        "month_lower": config.MONTH_LOWER
    }

    with open("selected_month.json", "w") as f:
        json.dump(settings, f, indent=4)

    total = len(scripts)

    for i, (name, script) in enumerate(scripts):

        if status_callback:
            status_callback(name)

        result = subprocess.run(
            [sys.executable, script],
            text=True
        )

        if result.returncode != 0:
            raise Exception(f"{name} failed.")

        if progress_callback:
            progress_callback((i + 1) / total)

    return True