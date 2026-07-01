import os
import sys

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import pandas as pd
import config
from bank_parser import extract_text, extract_lieferando_transactions

pdf_file = os.path.join(
    config.BANK_FOLDER,
    f"{config.MONTH}_Bank_Statement.pdf"
)

text = extract_text(pdf_file)

transactions = extract_lieferando_transactions(text)

rows = []

for date, amount in transactions:

    rows.append({
        "date": date,
        "description": "Lieferando",
        "amount": amount
    })

df = pd.DataFrame(rows)

os.makedirs(config.OUTPUT_FOLDER, exist_ok=True)

output_file = os.path.join(
    config.OUTPUT_FOLDER,
    f"{config.MONTH_LOWER}_lieferando.csv"
)

df.to_csv(output_file, index=False)

print(df)
print()
print("Lieferando rows:", len(df))
