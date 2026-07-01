import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent

if str(ROOT) not in sys.path:
    sys.path.append(str(ROOT))

import re
import pandas as pd
import config

# ---------------------------------------------
# LOAD OCR ROWS
# ---------------------------------------------

df = pd.read_csv("ocr_rows.csv")

transactions = []


# ---------------------------------------------
# CLEAN DATE
# ---------------------------------------------

def clean_date(text):

    text = text.upper()

    text = text.replace("OG", "09")
    text = text.replace("O9", "09")
    text = text.replace("O", "0")

    text = " ".join(text.split())

    match = re.search(r"(\d{2})\s*\.\s*(\d{2})\.", text)

    if match:
        return f"{match.group(1)}.{match.group(2)}."

    return ""


# ---------------------------------------------
# CLEAN AMOUNT
# ---------------------------------------------

def clean_amount(text):

    # Remove spaces around commas
    text = text.replace(" ,", ",")
    text = text.replace(", ", ",")

    # Find all money-like values
    amounts = re.findall(r"\d{1,3}(?:\.\d{3})?,\d{2}", text)

    if amounts:
        return amounts[-1]

    return ""


# ---------------------------------------------
# PARSE
# ---------------------------------------------

for i in range(len(df)):

    row = str(df.loc[i, "row"])

    if "DERDENGELDEN TAKEAWAYCOM" not in row:
        continue

    previous_row = str(df.loc[i - 1, "row"]) if i > 0 else ""

    date = clean_date(previous_row)
    amount = clean_amount(previous_row)

    if date == "" or amount == "":
        continue

    transactions.append(
        {
            "date": date,
            "description": "Lieferando",
            "amount": amount
        }
    )


# ---------------------------------------------
# EXPORT
# ---------------------------------------------

result = pd.DataFrame(transactions)

print(result)

output_file = f"Outputs/{config.MONTH_LOWER}_lieferando.csv"

result.to_csv(
    output_file,
    index=False
)

print()
print(f"Rows: {len(result)}")
print(f"Created: {output_file}")