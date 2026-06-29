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


if __name__ == "__main__":

    pdf_file = "Data/Bank/January_Bank_Statement.pdf"

    text = extract_text(pdf_file)

    nexi_transactions = extract_nexi_transactions(text)

    print("\nNEXI TRANSACTIONS\n")

    total = 0

    for date, amount in nexi_transactions:

        value = float(amount.replace(".", "").replace(",", "."))

        total += value

        print(date, value)

    print("\nCOUNT:", len(nexi_transactions))
    print("TOTAL:", round(total, 2))