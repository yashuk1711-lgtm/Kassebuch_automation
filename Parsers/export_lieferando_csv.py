import pandas as pd
from bank_parser import extract_text, extract_lieferando_transactions

pdf_file = "Data/Bank/January_Bank_Statement.pdf"

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

df.to_csv("Outputs/january_lieferando.csv", index=False)

print(df)
print()
print("Lieferando rows:", len(df))