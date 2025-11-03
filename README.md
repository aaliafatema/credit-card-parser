# Credit Card Statement Parser

This project is a simple web app built using Flask that allows users to upload credit card statements (PDFs) and extract key details such as card brand, last digits, statement period, and payment due date.

## Features
- Upload PDF statements.
- Parse details using `pdfplumber` and `pytesseract`.
- Clean and formatted output without JSON clutter.

## Tech Stack
- Python (Flask)
- HTML, CSS (Frontend)
- pdfplumber, pytesseract, pdf2image, Pillow

## How to Run
1. Clone this repository:
   ```bash
   git clone https://github.com/<your-username>/cc-parser.git
