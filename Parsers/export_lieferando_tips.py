import os
import sys

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import glob
import re
from collections import defaultdict

import fitz
import pandas as pd
import config

pdf_files = glob.glob(os.path.join(config.LIEFERANDO_FOLDER, "*.pdf"))

daily_tips = defaultdict(float)

for pdf_path in pdf_files:

    print("Reading:", pdf_path)

    doc = fitz.open(pdf_path)

    text = ""

    for page in doc:
        text += page.get_text()

    lines = text.splitlines()

    tips_section = False

    for i in range(len(lines) - 2):

        # Start parsing after tips section begins
        if "Trinkgelder erhalten" in lines[i]:
            tips_section = True
            continue

        if not tips_section:
            continue

        # Match date lines
        date_match = re.match(
            r"(\d{2})-(\d{2})-(\d{4}),",
            lines[i]
        )

        if not date_match:
            continue

        day, month, year = date_match.groups()

        # Skip transactions outside the selected month
        if config.MONTH_NUM and month != config.MONTH_NUM:
            continue

        amount_line = lines[i + 2].strip()

        try:
            amount = float(
                amount_line.replace(".", "").replace(",", ".")
            )
        except ValueError:
            continue

        key = f"{day}.{month}."

        daily_tips[key] += amount

rows = []

for date, amount in sorted(daily_tips.items()):

    rows.append({
        "date": date,
        "description": "Lieferando Trinkgelder",
        "amount": str(round(amount, 2)).replace(".", ",")
    })

df = pd.DataFrame(rows)

os.makedirs(config.OUTPUT_FOLDER, exist_ok=True)

output_file = os.path.join(
    config.OUTPUT_FOLDER,
    f"{config.MONTH_LOWER}_lieferando_tips.csv"
)

df.to_csv(output_file, sep=";", index=False)

print(df)
print()
print("Rows:", len(df))
