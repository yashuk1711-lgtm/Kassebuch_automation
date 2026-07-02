import os

import pandas as pd

import config
from Parsers.uber_parser import extract_uber_settlement


def run():

    rows = []

    for filename in os.listdir(config.UBER_FOLDER):

        if not filename.endswith(".pdf"):
            continue

        settlement = extract_uber_settlement(
            os.path.join(config.UBER_FOLDER, filename)
        )

        if not settlement:
            print(f"Skipping {filename}: could not find Auszahlungsdatum")
            continue

        # Filter by the real payout month (Auszahlungsdatum), not the
        # filename's issue date - a file issued in one month can carry
        # a payout that actually landed in the previous month.
        if config.MONTH_NUM and settlement["date"][5:7] != config.MONTH_NUM:
            continue

        rows.append({
            "date": settlement["date"],
            "amount": settlement["amount"],
            "tip": settlement["tip"]
        })

    df = pd.DataFrame(rows, columns=["date", "amount", "tip"])

    if not df.empty:
        df = df.sort_values("date")

    print(df)

    os.makedirs(config.OUTPUT_FOLDER, exist_ok=True)

    output_file = os.path.join(
        config.OUTPUT_FOLDER,
        f"{config.MONTH_LOWER}_uber.csv"
    )

    df.to_csv(
        output_file,
        index=False,
        sep=";",
        encoding="utf-8-sig"
    )


if __name__ == "__main__":
    run()
