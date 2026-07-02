import os
import glob
import re
from collections import defaultdict

import fitz
import pandas as pd
import config


def run():

    pdf_files = glob.glob(os.path.join(config.LIEFERANDO_FOLDER, "*.pdf"))

    daily_cash = defaultdict(float)

    for pdf_path in pdf_files:

        print("Reading:", pdf_path)

        doc = fitz.open(pdf_path)

        text = ""

        for page in doc:
            text += page.get_text()

        lines = text.splitlines()

        tips_start = len(lines)

        for i, line in enumerate(lines):
            if "Trinkgelder erhalten" in line:
                tips_start = i
                break

        order_lines = lines[:tips_start]

        for i in range(len(order_lines) - 2):

            date_match = re.match(
                r"(\d{2})-(\d{2})-(\d{4}),",
                order_lines[i]
            )

            if not date_match:
                continue

            day, month, year = date_match.groups()

            # Skip transactions outside the selected month
            if config.MONTH_NUM and month != config.MONTH_NUM:
                continue

            amount_line = order_lines[i + 2].strip()

            # Skip online orders (already settled via bank transfer)
            if "*" in amount_line:
                continue

            try:
                amount = float(
                    amount_line.replace(".", "").replace(",", ".")
                )
            except ValueError:
                continue

            key = f"{day}.{month}."

            daily_cash[key] += amount

    rows = []

    for date, amount in sorted(daily_cash.items()):

        rows.append({
            "date": date,
            "description": "Lieferando",
            "amount": str(round(amount, 2)).replace(".", ",")
        })

    df = pd.DataFrame(rows)

    os.makedirs(config.OUTPUT_FOLDER, exist_ok=True)

    output_file = os.path.join(
        config.OUTPUT_FOLDER,
        f"{config.MONTH_LOWER}_lieferando_cash.csv"
    )

    df.to_csv(output_file, sep=";", index=False)

    print(df)
    print()
    print("Rows:", len(df))


if __name__ == "__main__":
    run()
