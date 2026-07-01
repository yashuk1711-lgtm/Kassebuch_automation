import pandas as pd


# ----------------------------------------
# NORMALIZE OCR WORDS
# ----------------------------------------

def normalize_word(word):

    word = str(word).strip()

    replacements = {
        "NEX!I": "NEXI",
        "NEX|": "NEXI",
        "NEXL": "NEXI",
        "RUTTO": "BRUTTO",
        "RUTT0": "BRUTTO",
    }

    for old, new in replacements.items():
        word = word.replace(old, new)

    return word


# ----------------------------------------
# BUILD OCR ROWS
# ----------------------------------------

def build_rows():

    INPUT_FILE = "ocr_words.csv"
    OUTPUT_FILE = "ocr_rows.csv"
    Y_THRESHOLD = 8

    df = pd.read_csv(INPUT_FILE)

    # Remove empty words
    df = df[df["text"].notna()]
    df = df[df["text"].astype(str).str.strip() != ""]

    # Sort by page, Y, X
    df = df.sort_values(
        by=["page", "top", "left"]
    ).reset_index(drop=True)

    rows = []

    current_page = None
    current_y = None
    current_words = []

    for _, word in df.iterrows():

        page = word["page"]
        y = word["top"]

        clean_word = normalize_word(word["text"])

        # First word
        if current_page is None:
            current_page = page
            current_y = y

        # -----------------------------
        # New page
        # -----------------------------
        if page != current_page:

            if current_words:

                current_words.sort(key=lambda x: x[0])

                row_text = " ".join(
                    w for _, w in current_words
                )

                rows.append({
                    "page": current_page,
                    "y": current_y,
                    "row": row_text
                })

            current_words = []
            current_page = page
            current_y = y

        # -----------------------------
        # Same row
        # -----------------------------
        if abs(y - current_y) <= Y_THRESHOLD:

            if clean_word:

                current_words.append(
                    (
                        word["left"],
                        clean_word
                    )
                )

        # -----------------------------
        # New row
        # -----------------------------
        else:

            if current_words:

                current_words.sort(key=lambda x: x[0])

                row_text = " ".join(
                    w for _, w in current_words
                )

                rows.append({
                    "page": current_page,
                    "y": current_y,
                    "row": row_text
                })

            current_words = []

            if clean_word:

                current_words.append(
                    (
                        word["left"],
                        clean_word
                    )
                )

            current_y = y

    # -----------------------------
    # Last row
    # -----------------------------
    if current_words:

        current_words.sort(key=lambda x: x[0])

        row_text = " ".join(
            w for _, w in current_words
        )

        rows.append({
            "page": current_page,
            "y": current_y,
            "row": row_text
        })

    rows_df = pd.DataFrame(rows)

    rows_df.to_csv(
        OUTPUT_FILE,
        index=False
    )

    print(rows_df.head(20))
    print()
    print(f"Rows: {len(rows_df)}")
    print(f"Saved as {OUTPUT_FILE}")


# ----------------------------------------
# RUN DIRECTLY
# ----------------------------------------

if __name__ == "__main__":
    build_rows()