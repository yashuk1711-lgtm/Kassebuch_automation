import fitz

doc = fitz.open("Data/Bank/February_Bank_Statement.pdf")

text = ""

for page in doc:
    text += page.get_text()

print(text[:5000])

with open("fitz_output.txt", "w", encoding="utf-8") as f:
    f.write(text)