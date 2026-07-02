import pdfplumber
import pytesseract
import re

import paths

pytesseract.pytesseract.tesseract_cmd = paths.TESSERACT_CMD


def _extract_text(pdf_file):

    text = ""

    with pdfplumber.open(pdf_file) as pdf:

        for page in pdf.pages:

            image = page.to_image(resolution=300)

            page_text = pytesseract.image_to_string(
                image.original,
                lang="eng"
            )

            text += page_text + "\n"

    return text


def extract_uber_settlement(pdf_file):
    """
    Extracts the real payout date (Auszahlungsdatum - when the money
    actually lands in the bank; this is NOT the same as the report's
    issue date, which the filename is based on and can belong to a
    different month), the total payout amount (Gesamtauszahlung), and
    any tip amount (Trinkgeld) from an Uber Eats settlement PDF.
    """

    text = _extract_text(pdf_file)

    date_match = re.search(
        r"Auszahlungsdatum:\s*(\d{2})\.(\d{2})\.(\d{4})",
        text
    )

    if not date_match:
        return None

    day, month, year = date_match.groups()

    amount_match = re.search(
        r"Gesamtauszahlung\s*€?\s*([\d.,]+)",
        text
    )

    tip_match = re.search(
        r"Trinkgeld\s*€?\s*\+?\s*([\d.,]+)",
        text
    )

    return {
        "date": f"{year}-{month}-{day}",
        "amount": amount_match.group(1) if amount_match else None,
        "tip": tip_match.group(1) if tip_match else None,
    }


if __name__ == "__main__":

    pdf_file = "Data/Uber_Eats/2024-01-03 Uber Eats.pdf"

    print(extract_uber_settlement(pdf_file))
