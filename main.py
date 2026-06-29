import subprocess
import config
import json

print("=" * 50)
print("        KASSENBUCH AUTOMATION")
print("=" * 50)
print()

import config

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
config.MONTH_LOWER = months[choice].lower()
settings = {
    "month": config.MONTH,
    "month_lower": config.MONTH_LOWER
}

with open("selected_month.json", "w") as f:
    json.dump(settings, f, indent=4)

print(f"\nSelected Month: {config.MONTH}")
print(f"Working folder: {config.DATA_FOLDER}")
print()

print("Select Month\n")

for number, month in months.items():
    print(f"{number}. {month}")

choice = input("\nEnter month number: ")

if choice not in months:
    print("Invalid month selected.")
    exit()

config.MONTH = months[choice]

print(f"\nSelected Month: {config.MONTH}\n")

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