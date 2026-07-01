import pandas as pd

# -----------------------------
# LOAD OCR ROWS
# -----------------------------

df = pd.read_csv("ocr_rows.csv")

blocks = []

# -----------------------------
# BUILD BLOCKS
# -----------------------------

for i in range(len(df)):

    row = str(df.loc[i, "row"])

    if "NEXI" in row or "TAKEAWAYCOM" in row:

        start = max(0, i - 1)
        end = min(len(df), i + 4)

        block = []

        for j in range(start, end):
            block.append(str(df.loc[j, "row"]))

        blocks.append({
            "type": "NEXI" if "NEXI" in row else "LIEFERANDO",
            "start_row": i,
            "block": "\n".join(block)
        })

# -----------------------------
# EXPORT
# -----------------------------

blocks_df = pd.DataFrame(blocks)

blocks_df.to_csv(
    "transaction_blocks.csv",
    index=False
)

print(blocks_df.head())

print()
print("Blocks:", len(blocks_df))
print("Saved transaction_blocks.csv")