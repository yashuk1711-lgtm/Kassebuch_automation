import fitz
import re
from collections import defaultdict

pdf_path = "Data/Lieferando/2024-01-28 LieferandoH.pdf"

doc = fitz.open(pdf_path)

text = ""
for page in doc:
    text += page.get_text()

lines = text.splitlines()
for i, line in enumerate(lines):
    if "Trinkgelder erhalten" in line:
        print("TIPS START AT:", i)
tips_start = 154

order_lines = lines[:tips_start]

daily_cash = defaultdict(float)

for i in range(len(order_lines) - 2):

    date_match = re.match(
        r"(\d{2})-(\d{2})-(\d{4}),",
        order_lines[i]
    )

    if not date_match:
        continue

    amount_line = order_lines[i + 2].strip()

    # Skip online orders
    if "*" in amount_line:
        continue

    amount = float(
        amount_line.replace(".", "")
                   .replace(",", ".")
    )

    day = date_match.group(1)
    month = date_match.group(2)

    key = f"{day}.{month}."

    daily_cash[key] += amount

for date, amount in daily_cash.items():
    print(date, round(amount, 2))
    import pandas as pd

rows = []

for date, amount in daily_cash.items():

    rows.append({
        "date": date,
        "description": "Lieferando",
        "amount": str(amount).replace(".", ",")
    })

df = pd.DataFrame(rows)

df.to_csv(
    "Outputs/january_lieferando_cash.csv",
    sep=";",
    index=False
)

print(df)
print()
print("Rows:", len(df))