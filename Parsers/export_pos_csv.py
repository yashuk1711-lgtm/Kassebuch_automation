import os
import pandas as pd
from pos_parser import extract_text, extract_sales

folder = "Data/Income_Reports"

rows = []

for file in os.listdir(folder):

    if "Uber Eats" in file:
        continue

    if "Lieferando" in file:
        continue

    pdf_path = os.path.join(folder, file)

    text = extract_text(pdf_path)

    data = extract_sales(text)

    rows.append({
        "date": file.replace(".pdf", ""),
        "umsatz19": data["umsatz19"],
        "umsatz7": data["umsatz7"],
        "kartentrinkgeld": data["kartentrinkgeld"]
    })

df = pd.DataFrame(rows)

os.makedirs("Outputs", exist_ok=True)

output_file = "Outputs/january_pos.csv"

df.to_csv(output_file, index=False)

print(f"CSV saved: {output_file}")
print(df.head())
