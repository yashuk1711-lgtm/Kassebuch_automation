import pandas as pd

# Load POS data
pos_df = pd.read_csv("Outputs/january_pos.csv")

rows = []
lfd_nr = 1

for _, row in pos_df.iterrows():

    date = row["date"]

    # Umsatz 19%
    rows.append({
        "Lfd.Nr": lfd_nr,
        "Datum": date,
        "Beschreibung": "Umsatz 19%",
        "Eingang": row["umsatz19"],
        "Ausgang": ""
    })
    lfd_nr += 1

    # Umsatz 7%
    rows.append({
        "Lfd.Nr": lfd_nr,
        "Datum": date,
        "Beschreibung": "Umsatz 7%",
        "Eingang": row["umsatz7"],
        "Ausgang": ""
    })
    lfd_nr += 1

    # Karten Trinkgeld
    if row["kartentrinkgeld"] != "0,00":

        rows.append({
            "Lfd.Nr": lfd_nr,
            "Datum": date,
            "Beschreibung": "Karten Trinkgeld",
            "Eingang": "",
            "Ausgang": row["kartentrinkgeld"]
        })

        lfd_nr += 1

# Create dataframe
kassenbuch_df = pd.DataFrame(rows)

# Export
output_file = "Outputs/january_kassenbuch.csv"

kassenbuch_df.to_csv(output_file, index=False)

print("Created:", output_file)
print()
print(kassenbuch_df.head(20))