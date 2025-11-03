import pdfplumber
import re
import os
import json

def parse_statement(pdf_path):
    """
    Extracts key information from a credit card statement PDF.
    Returns a dictionary with cleaned and structured data.
    """

    if not os.path.exists(pdf_path):
        return {"error": "File not found"}

    text = ""
    try:
        with pdfplumber.open(pdf_path) as pdf:
            for page in pdf.pages:
                page_text = page.extract_text()
                if page_text:
                    text += "\n" + page_text
    except Exception as e:
        return {"error": f"Failed to read PDF: {e}"}

    # Initialize output dictionary
    data = {
        "_source_file": os.path.basename(pdf_path),
        "_ocr_used": False,
        "card_brand": None,
        "card_last4": None,
        "card_last4_masked": None,
        "statement_period": {"start": None, "end": None},
        "payment_due_date": None,
        "new_balance": None,
        "transactions_extracted_count": 0,
        "transactions": []
    }

    # --- Extract Card Brand ---
    brand_patterns = [
        r"HDFC\s*Bank", r"ICICI\s*Bank", r"SBI\s*Card", r"Axis\s*Bank",
        r"American\s*Express", r"AMEX", r"Citi\s*Bank", r"Standard\s*Chartered"
    ]
    for pat in brand_patterns:
        match = re.search(pat, text, re.IGNORECASE)
        if match:
            data["card_brand"] = match.group().strip()
            break

    # --- Extract last 4 digits ---
    match = re.search(r"\b(?:XXXX|xxxx|x{4,})[- ]?(\d{4})\b", text)
    if match:
        data["card_last4"] = match.group(1)
        data["card_last4_masked"] = f"XXXX-XXXX-XXXX-{match.group(1)}"

    # --- Extract statement period ---
    period_match = re.search(
        r"(\d{1,2}[/-][A-Za-z]{3,9}[/-]\d{2,4})\s*(?:to|–|-|—)\s*(\d{1,2}[/-][A-Za-z]{3,9}[/-]\d{2,4})",
        text)
    if period_match:
        data["statement_period"]["start"] = period_match.group(1)
        data["statement_period"]["end"] = period_match.group(2)

    # --- Extract payment due date ---
    due_match = re.search(r"Payment\s+Due\s+Date[:\-]?\s*([\d/ -A-Za-z]+)", text, re.IGNORECASE)
    if due_match:
        data["payment_due_date"] = due_match.group(1).strip()

    # --- Extract total/new balance ---
    balance_match = re.search(r"(?:Total\s+Amount\s+Due|New\s+Balance|Total\s+Outstanding)[:\-]?\s*₹?([\d,]+\.\d{2})", text, re.IGNORECASE)
    if balance_match:
        data["new_balance"] = "₹" + balance_match.group(1)

    # --- Extract transactions ---
    transactions = []
    lines = text.splitlines()
    for line in lines:
        # Sample pattern for transaction: "24/09/2023 AMAZON 500.00"
        txn_match = re.match(r"(\d{1,2}/\d{1,2}/\d{2,4})\s+([A-Za-z0-9 ,.&'-]+)\s+(-?\d{1,9}\.\d{2})", line.strip())
        if txn_match:
            transactions.append({
                "date": txn_match.group(1),
                "description": txn_match.group(2).strip(),
                "amount": txn_match.group(3)
            })

    data["transactions"] = transactions
    data["transactions_extracted_count"] = len(transactions)

    # --- Save parsed output ---
    output_dir = "parser_output"
    os.makedirs(output_dir, exist_ok=True)
    out_path = os.path.join(output_dir, os.path.basename(pdf_path).replace(".pdf", ".parsed.json"))
    with open(out_path, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2, ensure_ascii=False)

    return data


if __name__ == "__main__":
    # For direct testing from command line
    import sys
    if len(sys.argv) < 2:
        print("Usage: python cc_statement_parser.py <statement.pdf>")
    else:
        file_path = sys.argv[1]
        result = parse_statement(file_path)
        print(json.dumps(result, indent=2, ensure_ascii=False))
