import pytesseract
import pandas as pd

from pdf2image import convert_from_path

import paths

pytesseract.pytesseract.tesseract_cmd = paths.TESSERACT_CMD


# -----------------------------------------
# OCR FUNCTION
# -----------------------------------------

def pdf_to_words(pdf_path, output_file=None):

    if output_file is None:
        output_file = paths.OUTPUTS_DIR / "ocr_words.csv"

    images = convert_from_path(
        pdf_path,
        dpi=300,
        poppler_path=paths.POPPLER_PATH
    )

    rows = []

    for page_number, image in enumerate(images, start=1):

        print(f"OCR Page {page_number}/{len(images)}")

        data = pytesseract.image_to_data(
            image,
            output_type=pytesseract.Output.DICT,
            lang="eng"
        )

        for i in range(len(data["text"])):

            word = data["text"][i].strip()

            if not word:
                continue

            rows.append({
                "page": page_number,
                "text": word,
                "left": data["left"][i],
                "top": data["top"][i],
                "width": data["width"][i],
                "height": data["height"][i],
                "conf": data["conf"][i]
            })

    df = pd.DataFrame(rows)

    paths.OUTPUTS_DIR.mkdir(parents=True, exist_ok=True)

    df.to_csv(output_file, index=False)

    print()
    print("Words:", len(df))
    print("Created:", output_file)
