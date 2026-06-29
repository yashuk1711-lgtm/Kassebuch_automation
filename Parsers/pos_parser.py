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


def extract_sales(text):

    vat19 = re.search(r"Gesamt 19\.0%\s+([\d.,]+)", text)
    vat7 = re.search(r"Gesamt 7\.0%\s+([\d.,]+)", text)
    tip = re.search(r"Sonstiges Trinkgeld\s+([\d.,]+)", text)

    result = {
        "umsatz19": vat19.group(1) if vat19 else None,
        "umsatz7": vat7.group(1) if vat7 else None,
        "kartentrinkgeld": tip.group(1) if tip else None
    }

    return result


if __name__ == "__main__":

    pdf_file = "Data/Income_Reports/2024-01-23.pdf"

    text = extract_text(pdf_file)

    data = extract_sales(text)

    transactions = [
        {
            "description": "Umsatz 19%",
            "income": float(data["umsatz19"].replace(",", ".")),
            "expense": 0
        },
        {
            "description": "Umsatz 7%",
            "income": float(data["umsatz7"].replace(",", ".")),
            "expense": 0
        },
        {
            "description": "Karten Trinkgeld",
            "income": 0,
            "expense": float(data["kartentrinkgeld"].replace(",", "."))
        }
    ]

    for transaction in transactions:
        print(transaction)