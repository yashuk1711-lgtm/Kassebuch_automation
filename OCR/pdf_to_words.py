import pytesseract
import pandas as pd

from pdf2image import convert_from_path

# -----------------------------------------
# CONFIGURATION
# -----------------------------------------

pytesseract.pytesseract.tesseract_cmd = (
    r"C:\Program Files\Tesseract-OCR\tesseract.exe"
)

POPPLER_PATH = r"C:\poppler\poppler-26.02.0\Library\bin"


# -----------------------------------------
# OCR FUNCTION
# -----------------------------------------

def pdf_to_words(pdf_path):

    images = convert_from_path(
        pdf_path,
        dpi=300,
        poppler_path=POPPLER_PATH
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

    df.to_csv(
        "ocr_words.csv",
        index=False
    )

    print()
    print("Words:", len(df))
    print("Created: ocr_words.csv")