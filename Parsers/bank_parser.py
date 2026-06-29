import pdfplumber
import re


def extract_text(pdf_path):
    text = ""

    with pdfplumber.open(pdf_path) as pdf:
        for page in pdf.pages:

            page_text = page.extract_text()

            if page_text:
                text += page_text + "\n"

    return text


def extract_nexi_transactions(text):

    pattern = r"(\d{2}\.\d{2}\.)\s+\d{2}\.\d{2}\.\s+UEBERWEISUNGSGUTSCHR.*?NEXI GERMANY GMBH.*?RUTTO([\d.,]+)"

    matches = re.findall(pattern, text, re.DOTALL)

    return matches

def extract_lieferando_transactions(text):

    lines = text.splitlines()
    transactions = []

    for i, line in enumerate(lines):

        if "DERDENGELDEN TAKEAWAYCOM" not in line:
            continue

        # The payment line is immediately above TAKEAWAYCOM
        if i == 0:
            continue

        payment_line = lines[i - 1]

        match = re.search(
            r"(\d{2}\.\d{2}\.)\s+\d{2}\.\d{2}\.\s+UEBERWEISUNGSGUTSCHR.*?([\d.,]+)\s+H",
            payment_line,
        )

        if match:
            transactions.append((match.group(1), match.group(2)))

    return transactions