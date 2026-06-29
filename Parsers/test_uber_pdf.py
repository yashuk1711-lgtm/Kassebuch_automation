import fitz

pdf = fitz.open("Data/Uber_Eats/2024-01-03 Uber Eats.pdf")

for i, page in enumerate(pdf):

    print(f"\n===== PAGE {i+1} =====")

    text = page.get_text()

    print(repr(text[:1000]))