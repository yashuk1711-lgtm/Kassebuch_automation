import pandas as pd
print("=== GENERATE_FULL_KASSENBUCH STARTED ===")
# Load files
pos_df = pd.read_csv("Outputs/january_pos.csv")
nexi_df = pd.read_csv("Outputs/january_nexi.csv")

lieferando_cash_df = pd.read_csv(
    "Outputs/january_lieferando_cash.csv",
    sep=";"
)

lieferando_tips_df = pd.read_csv(
    "Outputs/january_lieferando_tips.csv",
    sep=";"
)
uber_df = pd.read_csv("Outputs/uber.csv", sep=";")
manual_df = pd.read_csv(
    "Outputs/manual_expenses.csv",
    sep=";"
)
print("MANUAL DF LOADED")
print(manual_df)
rows = []
lfd_nr = 1
starting_balance = 42876.01

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

    # DEBUG
    if day in ["16", "20", "22", "25", "26"]:
        print("\nDEBUG TIP MATCH")
        print("day_month =", repr(day_month))
        print("csv dates =", lieferando_tips_df["date"].tolist())

    # Lieferando Tips
    matching_tips = lieferando_tips_df[
        lieferando_tips_df["date"] == day_month
    ]

    if day in ["16", "20", "22", "25", "26"]:
        print("matches:")
        print(matching_tips)

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

            print(
                "FOUND MANUAL EXPENSE:",
                expense["description"],
                expense["amount"]
            )

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

output_file = "Outputs/january_kassenbuch_full.csv"

df.to_csv(output_file, index=False)

print("Created:", output_file)
print("Rows:", len(df))
print(df.head(25))