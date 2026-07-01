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

    # OCR corrections
    text = text.replace("OG", "09")
    text = text.replace("O9", "09")
    text = text.replace("O", "0")

    # Remove duplicate spaces
    text = " ".join(text.split())

    # Extract first DD.MM.
    match = re.search(r"(\d{2})\s*\.\s*(\d{2})\.", text)

    if match:
        return f"{match.group(1)}.{match.group(2)}."

    return ""


# ---------------------------------------------
# CLEAN AMOUNT
# ---------------------------------------------

def clean_amount(text):

    text = text.replace(" ", "")

    match = re.search(r"BRUTTO([0-9.,]+)", text)

    if not match:
        return ""

    amount = match.group(1)

    # Remove thousand separator
    amount = amount.replace(".", "")

    # OCR sometimes gives:
    # 87540
    # instead of
    # 875,40
    if "," not in amount and len(amount) > 2:
        amount = amount[:-2] + "," + amount[-2:]

    return amount


# ---------------------------------------------
# PARSE TRANSACTIONS
# ---------------------------------------------

for i in range(len(df)):

    row = str(df.loc[i, "row"])

    # Only NEXI settlements
    if "NEXI GERMANY GMBH" not in row:
        continue

    first_row = str(df.loc[i - 1, "row"]) if i > 0 else ""

    # Skip monthly fee transaction
    if "BASISLASTSCHRIFT" in first_row:
        continue

    brutto_row = ""

    # Search next few rows for BRUTTO
    for j in range(i + 1, min(i + 4, len(df))):

        candidate = str(df.loc[j, "row"])

        if "BRUTTO" in candidate:
            brutto_row = candidate
            break

    date = clean_date(first_row)
    amount = clean_amount(brutto_row)

    # Skip incomplete OCR results
    if date == "" or amount == "":
        continue

    transactions.append(
        {
            "date": date,
            "description": "NEXI GERMANY GMBH",
            "amount": amount
        }
    )


# ---------------------------------------------
# EXPORT
# ---------------------------------------------

result = pd.DataFrame(transactions)

print(result)

output_file = f"Outputs/{config.MONTH_LOWER}_nexi.csv"

result.to_csv(
    output_file,
    index=False
)

print()
print(f"Rows: {len(result)}")
print(f"Created: {output_file}")