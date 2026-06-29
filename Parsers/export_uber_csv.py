import os
import pandas as pd

from uber_parser import extract_uber_amount

folder = "Data/Uber_Eats"

rows = []

for filename in os.listdir(folder):

    if not filename.endswith(".pdf"):
        continue

    amount = extract_uber_amount(
        os.path.join(folder, filename)
    )

    date = filename[:10]

    rows.append({
        "date": date,
        "description": "Uber Eats",
        "amount": amount
    })

df = pd.DataFrame(rows)

df = df.sort_values("date")

print(df)

df.to_csv(
    "Outputs/uber.csv",
    index=False,
    sep=";",
    encoding="utf-8-sig"
)