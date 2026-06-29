import pandas as pd
from bank_parser import extract_text, extract_nexi_transactions

pdf_file = "Data/Bank/January_Bank_Statement.pdf"

text = extract_text(pdf_file)

transactions = extract_nexi_transactions(text)

rows = []

for date, amount in transactions:

    if amount == "0,00":
        continue

    rows.append({
        "date": date,
        "description": "NEXI GERMANY GMBH",
        "amount": amount
    })

df = pd.DataFrame(rows)

df.to_csv("Outputs/january_nexi.csv", index=False)

print(df.head())
print()
print("NEXI rows:", len(df))