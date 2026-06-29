import os
import sys

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import os
import pandas as pd
import config
from pos_parser import extract_text, extract_sales


def run():

    folder = config.INCOME_REPORTS_FOLDER

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