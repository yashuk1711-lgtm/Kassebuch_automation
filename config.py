import os
import json

DATA_FOLDER = "Data"
OUTPUT_FOLDER = "Outputs"

BANK_FOLDER = os.path.join(DATA_FOLDER, "Bank")
INCOME_REPORTS_FOLDER = os.path.join(DATA_FOLDER, "Income_Reports")
LIEFERANDO_FOLDER = os.path.join(DATA_FOLDER, "Lieferando")
UBER_FOLDER = os.path.join(DATA_FOLDER, "Uber")

MANUAL_FOLDER = os.path.join(DATA_FOLDER, "Manual")

MONTH = ""
MONTH_LOWER = ""
MONTH_NUM = ""
STARTING_BALANCE = None

if os.path.exists("settings.json"):

    with open("settings.json", "r") as f:
        settings = json.load(f)

    MONTH = settings.get("month", "")
    MONTH_LOWER = settings.get("month_lower", "")
    MONTH_NUM = settings.get("month_num", "")
    STARTING_BALANCE = settings.get("starting_balance")