import fitz
import pandas as pd
import re
import glob
from collections import defaultdict

# Find all Lieferando PDFs
pdf_files = glob.glob("Data/Lieferando/*.pdf")

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

        if date_match:
            print("DATE FOUND:", lines[i])

        if not date_match:
            continue

        amount_line = lines[i + 2].strip()

        try:
            amount = float(
                amount_line.replace(".", "")
                           .replace(",", ".")
            )
        except:
            continue

        day = date_match.group(1)
        month = date_match.group(2)

        key = f"{day}.{month}."

        print("TIP:", key, amount)

        daily_tips[key] += amount

print("\nDAILY TIPS:")
print(dict(daily_tips))

rows = []

for date, amount in sorted(daily_tips.items()):

    rows.append({
        "date": date,
        "description": "Lieferando Trinkgelder",
        "amount": str(round(amount, 2)).replace(".", ",")
    })

df = pd.DataFrame(rows)

df.to_csv(
    "Outputs/january_lieferando_tips.csv",
    sep=";",
    index=False
)

print("\nRESULT:")
print(df)

print("\nRows:", len(df))
print("\nCreated: Outputs/january_lieferando_tips.csv")