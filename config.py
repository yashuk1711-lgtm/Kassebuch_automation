import json

import paths

DATA_FOLDER = paths.DATA_DIR
OUTPUT_FOLDER = paths.OUTPUTS_DIR

BANK_FOLDER = DATA_FOLDER / "Bank"
INCOME_REPORTS_FOLDER = DATA_FOLDER / "Income_Reports"
LIEFERANDO_FOLDER = DATA_FOLDER / "Lieferando"
UBER_FOLDER = DATA_FOLDER / "Uber_Eats"
MANUAL_FOLDER = DATA_FOLDER / "Manual"

RESTAURANT_NAME = "Athidhi Restaurant"

SETTINGS_FILE = paths.BASE_DIR / "settings.json"

MONTH = ""
MONTH_LOWER = ""
MONTH_NUM = ""
STARTING_BALANCE = None


def _load():

    global MONTH, MONTH_LOWER, MONTH_NUM, STARTING_BALANCE

    if not SETTINGS_FILE.exists():
        return

    with open(SETTINGS_FILE, "r") as f:
        settings = json.load(f)

    MONTH = settings.get("month", "")
    MONTH_LOWER = settings.get("month_lower", "")
    MONTH_NUM = settings.get("month_num", "")
    STARTING_BALANCE = settings.get("starting_balance")


def set_month(month, month_num, starting_balance):
    """Select the active month, persist it to settings.json, and update
    this module's globals in place so already-imported code sees it."""

    global MONTH, MONTH_LOWER, MONTH_NUM, STARTING_BALANCE

    MONTH = month
    MONTH_LOWER = month.lower()
    MONTH_NUM = month_num
    STARTING_BALANCE = starting_balance

    with open(SETTINGS_FILE, "w") as f:
        json.dump({
            "month": MONTH,
            "month_lower": MONTH_LOWER,
            "month_num": MONTH_NUM,
            "starting_balance": STARTING_BALANCE
        }, f, indent=4)


_load()
