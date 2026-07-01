import pandas as pd

# ---------------------------------
# LOAD OCR ROWS
# ---------------------------------

df = pd.read_csv("ocr_rows.csv")

print("Total rows:", len(df))
print()

# ---------------------------------
# FIND NEXI BLOCKS
# ---------------------------------

for i in range(len(df)):

    row = str(df.loc[i, "row"])

    if "NEXI" not in row:
        continue

    print("=" * 80)
    print(f"NEXI found at row {i}")
    print()

    start = max(0, i - 1)
    end = min(len(df), i + 4)

    for j in range(start, end):
        print(df.loc[j, "row"])

    print()