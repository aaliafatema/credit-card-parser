from flask import Flask, render_template, request
import json
from statementparser import parse_statement
import os

app = Flask(__name__)

UPLOAD_FOLDER = "uploads"
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        file = request.files["pdf_file"]
        if not file:
            return "No file uploaded.", 400

        filepath = os.path.join(UPLOAD_FOLDER, file.filename)
        file.save(filepath)

        result = parse_statement(filepath)

        # Convert result to dictionary if it's a JSON string
        if isinstance(result, str):
            try:
                result = json.loads(result)
            except json.JSONDecodeError:
                result = {"error": "Failed to parse statement"}

        return render_template("result.html", result=result)

    return render_template("index.html")


if __name__ == "__main__":
    app.run(debug=True)
