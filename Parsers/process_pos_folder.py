import os
from pos_parser import extract_text, extract_sales

folder = "Data/Income_Reports"

all_transactions = []

for file in os.listdir(folder):

    if "Uber Eats" in file:
        continue

    if "Lieferando" in file:
        continue

    pdf_path = os.path.join(folder, file)

    text = extract_text(pdf_path)

    data = extract_sales(text)

    print(file)
    print(data)
    print("-" * 40)

    all_transactions.append({
        "date": file.replace(".pdf", ""),
        "umsatz19": data["umsatz19"],
        "umsatz7": data["umsatz7"],
        "kartentrinkgeld": data["kartentrinkgeld"]
    })

print("\nTOTAL POS REPORTS:", len(all_transactions))