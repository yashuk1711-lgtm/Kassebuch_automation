import os

import pandas as pd

import config
from Parsers.pos_parser import extract_text, extract_sales


def run():

    folder = config.INCOME_REPORTS_FOLDER

    rows = []

    # Month number mapping
    month_numbers = {
        "january": "01",
        "february": "02",
        "march": "03",
        "april": "04",
        "may": "05",
        "june": "06",
        "july": "07",
        "august": "08",
        "september": "09",
        "october": "10",
        "november": "11",
        "december": "12"
    }

    selected_month = month_numbers[config.MONTH_LOWER]

    for file in os.listdir(folder):

        if not file.endswith(".pdf"):
            continue

        # Ignore Uber and Lieferando reports
        if "Uber Eats" in file:
            continue

        if "Lieferando" in file:
            continue

        # Only process selected month
        if f"-{selected_month}-" not in file:
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

    os.makedirs(config.OUTPUT_FOLDER, exist_ok=True)

    output_file = os.path.join(
        config.OUTPUT_FOLDER,
        f"{config.MONTH_LOWER}_pos.csv"
    )

    df.to_csv(output_file, index=False)

    print(f"CSV saved: {output_file}")
    print(df.head())


if __name__ == "__main__":
    run()
