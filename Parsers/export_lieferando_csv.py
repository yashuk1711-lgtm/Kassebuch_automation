import pdfplumber


def extract_text(pdf_path):
    text = ""

    with pdfplumber.open(pdf_path) as pdf:
        for page in pdf.pages:
            page_text = page.extract_text()

            if page_text:
                text += page_text + "\n"

    return text


pdf_file = "Data/Bank/January_Bank_Statement.pdf"

text = extract_text(pdf_file)

lines = text.split("\n")

for i, line in enumerate(lines):

    if "TAKEAWAYCOM" in line:

        print("\n" + "=" * 50)

        start = max(0, i - 3)
        end = min(len(lines), i + 4)

        for j in range(start, end):
            print(lines[j])