import subprocess
import json
import os

import config
import pandas as pd

print("=" * 50)
print("        KASSENBUCH AUTOMATION")
print("=" * 50)
print()

months = {
    "1": "January",
    "2": "February",
    "3": "March",
    "4": "April",
    "5": "May",
    "6": "June",
    "7": "July",
    "8": "August",
    "9": "September",
    "10": "October",
    "11": "November",
    "12": "December"
}

print("Select Month\n")

for number, month in months.items():
    print(f"{number}. {month}")

choice = input("\nEnter month number: ")

if choice not in months:
    print("Invalid month selected.")
    exit()

config.MONTH = months[choice]
config.MONTH_LOWER = config.MONTH.lower()
config.MONTH_NUM = choice.zfill(2)

# Carry the closing balance of the previous month forward as this
# month's opening balance. Falls back to a manual prompt when no
# previous month has been generated yet (e.g. the very first run).
starting_balance = None
prev_choice = str(int(choice) - 1)

if prev_choice in months:

    prev_month_lower = months[prev_choice].lower()

    prev_kassenbuch = os.path.join(
        config.OUTPUT_FOLDER,
        f"{prev_month_lower}_kassenbuch_full.csv"
    )

    if os.path.exists(prev_kassenbuch):
        prev_df = pd.read_csv(prev_kassenbuch)
        starting_balance = round(float(prev_df.iloc[-1]["Neuestand"]), 2)
        print(f"\nFound {months[prev_choice]}'s Kassenbuch — carrying "
              f"forward closing balance: {starting_balance}")

if starting_balance is None:
    raw = input(
        f"\nNo previous month found. Enter starting balance "
        f"(Anfangsbestand) for {config.MONTH}: "
    )
    starting_balance = float(raw.replace(".", "").replace(",", "."))

settings = {
    "month": config.MONTH,
    "month_lower": config.MONTH_LOWER,
    "month_num": config.MONTH_NUM,
    "starting_balance": starting_balance
}

with open("settings.json", "w") as f:
    json.dump(settings, f, indent=4)

config.STARTING_BALANCE = starting_balance

print(f"\nSelected Month: {config.MONTH}")
print(f"Working folder: {config.DATA_FOLDER}")
print()

scripts = [
    ("POS Export", "Parsers/export_pos_csv.py"),
    ("NEXI Export", "Parsers/export_nexi_csv.py"),
    ("Lieferando Bank Export", "Parsers/export_lieferando_csv.py"),
    ("Lieferando Cash Export", "Parsers/export_lieferando_cash.py"),
    ("Lieferando Tips Export", "Parsers/export_lieferando_tips.py"),
    ("Uber Export", "Parsers/export_uber_csv.py"),
    ("Generate Kassenbuch", "Parsers/generate_full_kassenbuch.py")
]

for name, script in scripts:

    print(f"Running {name}...")

    result = subprocess.run(
        ["python", script],
        text=True
    )

    if result.returncode == 0:
        print("✓ Success\n")
    else:
        print("✗ Failed")
        break

print("=" * 50)
print("Automation Finished")
print("=" * 50)
