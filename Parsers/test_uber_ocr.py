import pdfplumber
import pytesseract
from PIL import Image

pytesseract.pytesseract.tesseract_cmd = (
    r"C:\Program Files\Tesseract-OCR\tesseract.exe"
)

pdf_file = "Data/Uber_Eats/2024-01-03 Uber Eats.pdf"

with pdfplumber.open(pdf_file) as pdf:

    page = pdf.pages[0]

    image = page.to_image(resolution=300)

    pil_image = image.original

    text = pytesseract.image_to_string(
        pil_image,
        lang="eng"
    )

    print(text)