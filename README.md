🧾 Credit Card Statement Parser
📌 Overview

The Credit Card Statement Parser is a Flask-based web application that extracts key information from credit card statement PDFs. It helps users easily view essential financial details without manually scanning through their statements.

This project supports statements from multiple issuers and provides a simple, user-friendly web interface where anyone can upload a statement and get structured data instantly.

⚙️ Features

🧠 Automatic PDF Parsing: Reads and processes real-world credit card statements.

💳 Issuer Flexibility: Works with 5 major credit card providers.

📄 Key Data Extraction: Retrieves card type, last 4 digits, statement period, due date, and transaction summary.

🌐 Web Interface: Upload PDFs directly from your browser.

🎨 Styled Output: Clean and modern display without raw JSON formatting.

🛠️ Tech Stack

Python 3

Flask (for the web app)

pdfplumber (for text extraction from PDFs)

pytesseract + pdf2image (for OCR-based reading when needed)

HTML/CSS (for frontend design)

🚀 How to Run Locally

Clone this repository:

git clone https://github.com/aaliafatema/credit-card-parser.git
cd credit-card-parser


Install dependencies:

pip install flask pdfplumber pytesseract pdf2image pillow


Run the Flask app:

python app.py


Open in your browser:

http://127.0.0.1:5000/


Upload your PDF and view the parsed results beautifully formatted.

🧩 Project Structure
credit-card-parser/
│
├── app.py                     # Flask web app
├── cc_statement_parser.py     # PDF parsing logic
│
├── templates/
│   ├── index.html             # Upload page
│   └── result.html            # Output display page
│
├── static/
│   └── style.css              # Styling for frontend
│
├── uploads/                   # Temporary storage for uploaded PDFs
└── README.md

📚 Example Output

Input: hdfc.pdf
Output (displayed in browser):

Card Brand: Rewards
Card Number: XXXX-XXXX-XXXX-9008
Statement Period: 24/08/2018 - 23/09/2018
Payment Due Date: 11/10/2018
Transactions Extracted: 51

👩‍💻 Author

Aalia Fatema Dandawala
Credit Card Statement Parser — Assignment Project
