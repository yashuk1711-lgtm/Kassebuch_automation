import os
import sys

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import pandas as pd
import config

print("=== GENERATE_FULL_KASSENBUCH STARTED ===")

if config.STARTING_BALANCE is None:
    raise SystemExit(
        "No starting balance found in settings.json. "
        "Run main.py to select a month first."
    )


def output_path(name):
    return os.path.join(config.OUTPUT_FOLDER, f"{config.MONTH_LOWER}_{name}.csv")


def read_csv_if_exists(path, **kwargs):
    if os.path.exists(path):
        return pd.read_csv(path, **kwargs)
    return pd.DataFrame(columns=["date", "description", "amount"])


# Load files
pos_df = pd.read_csv(output_path("pos"))
nexi_df = pd.read_csv(output_path("nexi"))
lieferando_cash_df = pd.read_csv(output_path("lieferando_cash"), sep=";")
lieferando_tips_df = pd.read_csv(output_path("lieferando_tips"), sep=";")
uber_df = pd.read_csv(output_path("uber"), sep=";")

manual_expenses_file = os.path.join(
    config.MANUAL_FOLDER,
    f"{config.MONTH_LOWER}_manual_expenses.csv"
)

manual_df = read_csv_if_exists(manual_expenses_file, sep=";")

rows = []
lfd_nr = 1
starting_balance = config.STARTING_BALANCE

for _, pos in pos_df.iterrows():

    date = str(pos["date"])

    if "/" in date:
        day, month, year = date.split("/")

    elif "-" in date:
        year, month, day = date.split("-")

    else:
        print("BAD DATE:", repr(date))
        continue

    formatted_date = f"{int(day)}.{int(month)}.{year}"
    day_month = f"{day.zfill(2)}.{month.zfill(2)}."

    # Umsatz 19%
    rows.append({
        "Lfd.Nr": lfd_nr,
        "Datum": formatted_date,
        "Beschreibung": "Umsatz 19%",
        "Eingang": pos["umsatz19"],
        "Ausgang": ""
    })
    lfd_nr += 1

    # Umsatz 7%
    rows.append({
        "Lfd.Nr": lfd_nr,
        "Datum": formatted_date,
        "Beschreibung": "Umsatz 7%",
        "Eingang": pos["umsatz7"],
        "Ausgang": ""
    })
    lfd_nr += 1

    # Karten Trinkgeld
    if str(pos["kartentrinkgeld"]) != "0,00":

        rows.append({
            "Lfd.Nr": lfd_nr,
            "Datum": formatted_date,
            "Beschreibung": "Karten Trinkgeld",
            "Eingang": "",
            "Ausgang": pos["kartentrinkgeld"]
        })

        lfd_nr += 1

    # NEXI
    matching_nexi = nexi_df[
        nexi_df["date"] == day_month
    ]

    for _, nexi in matching_nexi.iterrows():

        rows.append({
            "Lfd.Nr": lfd_nr,
            "Datum": formatted_date,
            "Beschreibung": "NEXI GERMANY GMBH",
            "Eingang": "",
            "Ausgang": nexi["amount"]
        })

        lfd_nr += 1

    # Lieferando Cash
    matching_cash = lieferando_cash_df[
        lieferando_cash_df["date"] == day_month
    ]

    for _, cash in matching_cash.iterrows():

        rows.append({
            "Lfd.Nr": lfd_nr,
            "Datum": formatted_date,
            "Beschreibung": "Lieferando",
            "Eingang": cash["amount"],
            "Ausgang": ""
        })

        lfd_nr += 1

    # Lieferando Tips
    matching_tips = lieferando_tips_df[
        lieferando_tips_df["date"] == day_month
    ]

    for _, tip in matching_tips.iterrows():

        rows.append({
            "Lfd.Nr": lfd_nr,
            "Datum": formatted_date,
            "Beschreibung": "Lieferando Trinkgelder",
            "Eingang": "",
            "Ausgang": tip["amount"]
        })

        lfd_nr += 1

    # Uber Eats
    uber_date = f"{year}-{month}-{day}"

    matching_uber = uber_df[
        uber_df["date"] == uber_date
    ]

    for _, uber in matching_uber.iterrows():

        rows.append({
            "Lfd.Nr": lfd_nr,
            "Datum": formatted_date,
            "Beschreibung": "Uber Eats",
            "Eingang": uber["amount"],
            "Ausgang": ""
        })

        lfd_nr += 1

    # Manual Expenses
    matching_manual = manual_df[
        manual_df["date"] == day_month
    ]

    for _, expense in matching_manual.iterrows():

        rows.append({
            "Lfd.Nr": lfd_nr,
            "Datum": formatted_date,
            "Beschreibung": expense["description"],
            "Eingang": "",
            "Ausgang": expense["amount"]
        })

        lfd_nr += 1

# Export
df = pd.DataFrame(rows)

balance = starting_balance
balances = []

for _, row in df.iterrows():

    income = row["Eingang"]
    expense = row["Ausgang"]

    if income != "":
        value = float(
            str(income)
            .replace(".", "")
            .replace(",", ".")
        )
        balance += value

    if expense != "":
        value = float(
            str(expense)
            .replace(".", "")
            .replace(",", ".")
        )
        balance -= value

    balances.append(round(balance, 2))

df["Neuestand"] = balances

os.makedirs(config.OUTPUT_FOLDER, exist_ok=True)

output_file = os.path.join(
    config.OUTPUT_FOLDER,
    f"{config.MONTH_LOWER}_kassenbuch_full.csv"
)

df.to_csv(output_file, index=False)

print("Created:", output_file)
print("Rows:", len(df))
print("Anfangsbestand:", starting_balance)
print("Endebestand:", balances[-1] if balances else starting_balance)
