import os
import sys

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import pandas as pd
import config
from uber_parser import extract_uber_amount

rows = []

for filename in os.listdir(config.UBER_FOLDER):

    if not filename.endswith(".pdf"):
        continue

    date = filename[:10]

    # Filename convention: YYYY-MM-DD ... .pdf
    if config.MONTH_NUM and date[5:7] != config.MONTH_NUM:
        continue

    amount = extract_uber_amount(
        os.path.join(config.UBER_FOLDER, filename)
    )

    rows.append({
        "date": date,
        "description": "Uber Eats",
        "amount": amount
    })

df = pd.DataFrame(rows)

if not df.empty:
    df = df.sort_values("date")

print(df)

os.makedirs(config.OUTPUT_FOLDER, exist_ok=True)

output_file = os.path.join(
    config.OUTPUT_FOLDER,
    f"{config.MONTH_LOWER}_uber.csv"
)

df.to_csv(
    output_file,
    index=False,
    sep=";",
    encoding="utf-8-sig"
)
