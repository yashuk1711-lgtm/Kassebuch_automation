import os
import pdfplumber
import pytesseract
import re

_WINDOWS_TESSERACT = r"C:\Program Files\Tesseract-OCR\tesseract.exe"

if os.name == "nt" and os.path.exists(_WINDOWS_TESSERACT):
    pytesseract.pytesseract.tesseract_cmd = _WINDOWS_TESSERACT


def extract_uber_amount(pdf_file):

    text = ""

    with pdfplumber.open(pdf_file) as pdf:

        for page in pdf.pages:

            image = page.to_image(resolution=300)

            page_text = pytesseract.image_to_string(
                image.original,
                lang="eng"
            )

            text += page_text + "\n"

    match = re.search(
        r"Gesamtauszahlung\s*€?\s*([\d.,]+)",
        text
    )

    if match:
        return match.group(1)

    return None


if __name__ == "__main__":

    pdf_file = "Data/Uber_Eats/2024-01-03 Uber Eats.pdf"

    amount = extract_uber_amount(pdf_file)

    print(amount)