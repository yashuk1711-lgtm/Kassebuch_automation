# Kassebuch_automation
# 📒 Kassenbuch Automation

## Overview

Kassenbuch Automation is a Python-based automation tool developed to simplify the creation of a German **Kassenbuch (Cash Book)**.

The application combines financial data from multiple sources, processes them automatically, and generates a complete Kassenbuch with a continuously calculated running balance (**Neuestand**).

The project was developed to reduce manual bookkeeping work, minimize errors, and speed up the monthly accounting process.

---

## Features

* ✅ Parse POS reports
* ✅ Import NEXI settlement transactions
* ✅ Import Uber Eats payments
* ✅ Import Lieferando payments
* ✅ Process Lieferando cash payments
* ✅ Process Lieferando card tips
* ✅ Add manual expenses (e.g., Lidl purchases)
* ✅ Generate VAT sales entries (7% & 19%)
* ✅ Automatically calculate running balance (Neuestand)
* ✅ Export final Kassenbuch as CSV

---

## Project Structure

```
Kassenbuch_Automation/
│
├── Parsers/
│   ├── bank_parser.py
│   ├── export_lieferando_cash.py
│   ├── export_lieferando_csv.py
│   ├── export_lieferando_tips.py
│   ├── export_nexi_csv.py
│   ├── export_pos_csv.py
│   ├── export_uber_csv.py
│   ├── generate_full_kassenbuch.py
│   ├── generate_kassenbuch.py
│   ├── lieferando_parser.py
│   ├── pos_parser.py
│   ├── process_pos_folder.py
│   └── uber_parser.py
│
├── Data/
├── Outputs/
├── main.py
├── run_month.py
└── README.md
```

---

## Workflow

```
POS Reports
        │
        ▼
 POS Parser
        │
        ▼
  January POS CSV
        │

NEXI Reports ─────────────► NEXI CSV

Uber Eats Statements ─────► Uber CSV

Lieferando Reports ───────► Lieferando CSV

Manual Expenses ──────────► Manual Expense CSV

                          │
                          ▼
          generate_full_kassenbuch.py
                          │
                          ▼
             Final Kassenbuch CSV
```

---

## Requirements

* Python 3.10+
* pandas
* pdfplumber
* PyMuPDF (`fitz`)
* pytesseract (plus the Tesseract OCR binary installed on your machine)
* openpyxl

Install dependencies:

```bash
pip install pandas pdfplumber PyMuPDF pytesseract openpyxl
```

---

## Usage

Drop the month's source PDFs into the matching `Data/` subfolder
(`Data/Bank`, `Data/Income_Reports`, `Data/Uber_Eats`, `Data/Lieferando`),
then run the monthly automation:

```bash
python main.py
```

This prompts you to pick the month, automatically carries forward the
previous month's closing balance as the new opening balance (or asks
for one manually if there's no previous month yet), and runs the full
parser → Kassenbuch pipeline.

`run_month.py` re-runs the same pipeline without prompting, reusing
whichever month was last selected via `main.py` (its selection is
stored in `settings.json`).

---

## Current Functionality

The automation currently supports:

* POS sales (7% and 19% VAT)
* Card tips
* NEXI settlements
* Uber Eats payments
* Lieferando payments
* Lieferando cash entries
* Lieferando card tips
* Manual expenses
* Running balance calculation

The generated output is exported as a CSV file ready for further accounting processing.

---

## Future Improvements

* Excel (.xlsx) export
* PDF report generation
* Configuration for different months
* Improved logging
* User interface (GUI)
* Support for multiple restaurants
* Automated validation checks

---

## Technologies Used

* Python
* Pandas
* CSV Processing
* Git
* GitHub

---

## Author

**Yashwanth Kurapati**

Master's Student – Interdisciplinary Engineering

This project was developed to automate the preparation of financial reports and reduce repetitive manual accounting tasks.
