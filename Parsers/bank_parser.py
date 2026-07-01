import pdfplumber
import pytesseract
import re

from pdf2image import convert_from_path

# -------------------------------------------------
# OCR Configuration
# -------------------------------------------------

pytesseract.pytesseract.tesseract_cmd = (
    r"C:\Program Files\Tesseract-OCR\tesseract.exe"
)

POPPLER_PATH = r"C:\poppler\poppler-26.02.0\Library\bin"


# -------------------------------------------------
# Extract Text
# -------------------------------------------------

def extract_text(pdf_path):

    text = ""

    try:

        with pdfplumber.open(pdf_path) as pdf:

            for page in pdf.pages:

                page_text = page.extract_text()

                if page_text:
                    text += page_text + "\n"

    except Exception:
        text = ""

    if len(text.strip()) > 1000:

        print("Using searchable PDF")

        return text

    print("Using OCR...")

    images = convert_from_path(
        pdf_path,
        dpi=300,
        poppler_path=POPPLER_PATH
    )

    text = ""

    for i, image in enumerate(images, start=1):

        print(f"OCR Page {i}/{len(images)}")

        page_text = pytesseract.image_to_string(
            image,
            lang="eng"
        )

        text += page_text + "\n"

    with open(
        "ocr_output.txt",
        "w",
        encoding="utf-8"
    ) as f:

        f.write(text)

    return text
# -------------------------------------------------
# Helper Functions
# -------------------------------------------------

def normalize_line(line):
    """
    Fix common OCR mistakes.
    """

    line = line.upper()

    # OCR mistakes
    line = line.replace("NEX!I", "NEXI")
    line = line.replace("NEX|", "NEXI")
    line = line.replace("NEXL", "NEXI")

    line = line.replace("UEBERWE |", "UEBERWE")
    line = line.replace("SUNGSGUTSCHR", "ISUNGSGUTSCHR")

    line = line.replace("RUTTO", "BRUTTO")

    # remove double spaces
    while "  " in line:
        line = line.replace("  ", " ")

    return line.strip()


def find_date(lines, index):
    """
    Search upwards to find the booking date.
    """

    for i in range(index, max(-1, index - 10), -1):

        line = normalize_line(lines[i])

        match = re.search(r"(\d{2}\.\d{2}\.)", line)

        if match:
            return match.group(1)

    return None


def find_brutto(lines, index):
    """
    Search nearby lines for BRUTTO amount.
    """

    for i in range(index, min(len(lines), index + 8)):

        line = normalize_line(lines[i])

        match = re.search(
            r"BRUTTO\s*([\d., ]+)",
            line
        )

        if match:

            amount = match.group(1)

            amount = amount.replace(" ", "")

            return amount

    return None


def contains_nexi(line):

    line = normalize_line(line)

    return (
        "NEXI GERMANY" in line
        or "NEXI" in line
    )


def contains_takeaway(line):

    line = normalize_line(line)

    return (
        "TAKEAWAY" in line
        or "LIEFERANDO" in line
    )
    # -------------------------------------------------
# NEXI Parser
# -------------------------------------------------

def extract_nexi_transactions(text):

    lines = text.splitlines()

    transactions = []

    i = 0

    while i < len(lines):

        line = normalize_line(lines[i])

        # Did we find a NEXI transaction?
        if contains_nexi(line):

            date = find_date(lines, i)

            amount = find_brutto(lines, i)

            if date and amount:

                # Remove spaces introduced by OCR
                amount = amount.replace(" ", "")

                # Remove accidental duplicate commas
                amount = amount.replace(",,", ",")

                # Skip zero amounts
                if amount not in ["0,00", "0.00", "0"]:

                    print(f"NEXI FOUND -> {date}  {amount}")

                    transactions.append(
                        (
                            date,
                            amount
                        )
                    )

        i += 1

    # Remove duplicates while preserving order
    unique = []

    seen = set()

    for t in transactions:

        if t not in seen:

            seen.add(t)

            unique.append(t)

    print(f"\nTotal NEXI transactions: {len(unique)}")

    return unique